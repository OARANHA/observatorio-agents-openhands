import asyncio
import unittest
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from canary_controls import GateError
from test_canary_transport_attempts import setup

class DeferredTransportTests(unittest.TestCase):
    def test_sync_iterator_is_denied_before_chunk_iteration(self):
        gate=setup();chunks=[]
        def stream():
            chunks.append('unexpected');yield 'fake'
        result=stream()
        with self.assertRaisesRegex(GateError,'deferred_transport_forbidden'):
            with gate.logical_call():gate.invoke(lambda:result)
        self.assertEqual([],chunks);self.assertTrue(gate.guard.cancelled)
        self.assertIsNotNone(gate.book.active)
        result.close()

    def test_sync_awaitable_is_denied_without_awaiting(self):
        gate=setup();chunks=[]
        async def deferred():chunks.append('unexpected');return 'fake'
        result=deferred()
        try:
            with self.assertRaisesRegex(GateError,'deferred_transport_forbidden'):
                with gate.logical_call():gate.invoke(lambda:result)
        finally:result.close()
        self.assertEqual([],chunks);self.assertTrue(gate.book.closed)

    def test_async_iterator_is_denied_before_chunk_iteration(self):
        gate=setup();chunks=[]
        async def stream():chunks.append('unexpected');yield 'fake'
        async def scenario():
            result=stream()
            async def fake():return result
            try:
                with self.assertRaisesRegex(GateError,'deferred_transport_forbidden'):
                    with gate.logical_call():await gate.ainvoke(fake)
            finally:await result.aclose()
        asyncio.run(scenario())
        self.assertEqual([],chunks);self.assertTrue(gate.guard.cancelled)
        self.assertIsNotNone(gate.book.active)

if __name__=='__main__':unittest.main(verbosity=2)

