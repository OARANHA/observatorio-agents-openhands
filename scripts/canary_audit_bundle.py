"""Bounded, versioned synthetic audit envelope; no operational authorization.

Integrity is an unkeyed checksum, NOT authenticity, attestation or replay defense.
No SDK import, environment read, file persistence, network or generic payloads.
"""
import copy
from datetime import datetime, timezone
from decimal import Decimal
import hashlib
import hmac
import json
import re
import uuid

from canary_accounting_evidence import synthetic_accounting_evidence
from canary_budget import exact_money
from canary_controls import GateError
from canary_transport_probe import SyntheticTransportGate

FIELDS=frozenset(('schema','classification','operational_go','authenticity_proven',
    'source_claim','source_sha','target_sdk','observed_at_utc','evidence_id',
    'accounting','sha256'))
MONEY=('book_budget_usd','verified_spent_usd','held_usd','book_uncommitted_usd')
COUNTS=('book_calls','guard_calls','guard_observed_input_tokens',
        'guard_observed_output_tokens')
REPORT_FIELDS=frozenset(('schema','operational_go','state',*MONEY,*COUNTS))


def _require(condition):
    if not condition:
        raise GateError('synthetic_audit_invalid')


def _canonical(data):
    return json.dumps(data,sort_keys=True,separators=(',',':'),
                      ensure_ascii=True,allow_nan=False).encode('ascii')


@exact_money
def verify_synthetic_audit_bundle(bundle):
    """Returns a detached validated copy. Never trusts a caller's GO or metadata."""
    try:
        _require(type(bundle) is dict and frozenset(bundle)==FIELDS)
        _require(bundle['schema']=='obs.synthetic.audit.v1'
                 and bundle['classification']=='synthetic'
                 and bundle['operational_go'] is False
                 and bundle['authenticity_proven'] is False
                 and bundle['source_claim']=='caller_declared_public_git_sha'
                 and bundle['target_sdk']=='1.53.0')
        sha=bundle['source_sha']
        _require(type(sha) is str and re.fullmatch('[0-9a-f]{40}',sha) is not None)
        ident=bundle['evidence_id']
        _require(type(ident) is str and len(ident)==46 and ident.startswith('SYNTHETIC-'))
        parsed=uuid.UUID(ident[10:])
        _require(parsed.version==4 and str(parsed)==ident[10:])
        stamp=bundle['observed_at_utc']
        _require(type(stamp) is str and re.fullmatch(
            r'[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z',stamp) is not None)
        datetime.strptime(stamp,'%Y-%m-%dT%H:%M:%SZ')
        report=bundle['accounting']
        _require(type(report) is dict and frozenset(report)==REPORT_FIELDS)
        _require(report['schema']=='obs.synthetic.accounting.v1'
                 and report['operational_go'] is False)
        amounts=[]
        for field in MONEY:
            value=report[field]
            _require(type(value) is str and len(value)<=64 and re.fullmatch(
                r'(?:0|[1-9][0-9]*)(?:\.[0-9]+)?',value) is not None)
            amounts.append(Decimal(value))
        budget,spent,held,remaining=amounts
        _require(budget>0 and budget==spent+held+remaining)
        for field in COUNTS:
            _require(type(report[field]) is int and 0<=report[field]<=10**18)
        _require(report['book_calls']<=report['guard_calls'])
        allowed=('closed_uncertain','open_reserved') if held>0 else (
            'closed_verified','open_idle')
        _require(report['state'] in allowed)
        digest=bundle['sha256']
        _require(type(digest) is str and re.fullmatch('[0-9a-f]{64}',digest) is not None)
        unsigned={k:v for k,v in bundle.items() if k!='sha256'}
        expected=hashlib.sha256(_canonical(unsigned)).hexdigest()
        _require(hmac.compare_digest(digest,expected))
        return copy.deepcopy(bundle)
    except (ValueError,TypeError,KeyError,ArithmeticError):
        raise GateError('synthetic_audit_invalid') from None


def synthetic_audit_bundle(gate, *, source_sha):
    """The public Git SHA is caller-declared, not verified against GitHub."""
    try:
        report=synthetic_accounting_evidence(gate)
        bundle={
            'schema':'obs.synthetic.audit.v1',
            'classification':'synthetic',
            'operational_go':False,
            'authenticity_proven':False,
            'source_claim':'caller_declared_public_git_sha',
            'source_sha':source_sha,
            'target_sdk':'1.53.0',
            'observed_at_utc':datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
            'evidence_id':'SYNTHETIC-'+str(uuid.uuid4()),
            'accounting':report,
        }
        # Validate the SHA before serializing any caller-supplied value.
        _require(type(source_sha) is str and re.fullmatch('[0-9a-f]{40}',source_sha) is not None)
        bundle['sha256']=hashlib.sha256(_canonical(bundle)).hexdigest()
        return verify_synthetic_audit_bundle(bundle)
    except BaseException:
        if isinstance(gate,SyntheticTransportGate):
            gate.book.abort(gate.guard)
        raise


def load_synthetic_audit_bundle(text):
    """Strict bounded JSON input; duplicate keys/NaN and unknown fields denied."""
    def pairs(items):
        result={}
        for key,value in items:
            _require(key not in result)
            result[key]=value
        return result
    def constant(_):
        raise GateError('synthetic_audit_invalid')
    _require(type(text) is str and len(text)<=8192)
    try:
        return verify_synthetic_audit_bundle(json.loads(text,
            object_pairs_hook=pairs,parse_constant=constant))
    except (ValueError,TypeError,RecursionError):
        raise GateError('synthetic_audit_invalid') from None
