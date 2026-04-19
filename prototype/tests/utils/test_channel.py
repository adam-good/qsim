import unittest
import utils.channel as chnl

class TestChannel(unittest.TestCase):
    def test_channel_send(self):
        data = 1
        channel = chnl.Channel()
        target = chnl.Channel((data,))
        result = chnl.send(channel, data)
        self.assertEqual(target, result)

    def test_channel_recv(self):
        channel = chnl.Channel((1,))
        target_data = 1
        target_channel_state = chnl.Channel()
        result, channel = chnl.recv(channel)
        self.assertEqual(result, target_data)
        self.assertEqual(target_channel_state, channel)
        
        
