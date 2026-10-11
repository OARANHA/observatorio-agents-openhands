"""Static distribution metadata only; never import SDK or dependency code."""
import importlib
from pathlib import Path
import sys
import types
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))


class DependencyInventory(unittest.TestCase):
    def api(self):
        self.assertIsNotNone(importlib.util.find_spec('audit_canary_dependencies'),
                             'dependency inventory contract missing')
        return importlib.import_module('audit_canary_dependencies')

    def fake(self,name):
        version='1.53.0' if name.startswith('openhands-') else '1.2.3'
        return types.SimpleNamespace(version=version,
            read_text=lambda _: 'Name: '+name+'\nVersion: '+version+'\n')

    def test_inventory_is_closed_minimized_and_always_offline(self):
        api=self.api();report=api.inventory(self.fake)
        self.assertEqual({'schema','operational_go','packages'},set(report))
        self.assertIs(report['operational_go'],False)
        self.assertEqual(list(api.PACKAGES),[r['name'] for r in report['packages']])
        for record in report['packages']:
            self.assertEqual({'name','version','metadata_sha256'},set(record))
            self.assertRegex(record['metadata_sha256'],'^[0-9a-f]{64}$')
        self.assertNotIn('Name:',str(report))

    def test_missing_metadata_and_sdk_drift_fail_closed(self):
        api=self.api()
        for name in api.PACKAGES:
            with self.subTest(name=name):
                def missing(selected):
                    obj=self.fake(selected)
                    if selected==name:obj.read_text=lambda _:None
                    return obj
                with self.assertRaisesRegex(api.GateError,'^dependency_inventory_invalid$'):
                    api.inventory(missing)
        def drift(name):
            obj=self.fake(name)
            if name=='openhands-sdk':obj.version='1.54.0'
            return obj
        with self.assertRaises(api.GateError):api.inventory(drift)

    def test_private_or_noncanonical_versions_are_never_emitted(self):
        api=self.api()
        for version in ('secret=value','١.2.3',True,'1.2.3+PRIVATE','1'*100):
            def invalid(name):
                obj=self.fake(name)
                if name=='aiohttp':obj.version=version
                return obj
            with self.assertRaisesRegex(api.GateError,'^dependency_inventory_invalid$'):
                api.inventory(invalid)
