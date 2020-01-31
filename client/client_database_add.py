from client import MQTTClient as mc
import json
import time


class MQTTClient(mc):
    def on_message(self, client, userdata, message):
        if message.topic == self.name:
            msg = json.loads(str(message.payload.decode('utf-8')))
            if not self.authorized:
                self.authLogic(msg)
            else:
                self.msg = msg
        else:
            print('message that was not intended for you has been received')

    def sendTag(self, tagId, msg):
        self.msg = msg
        self.sendPublish('RT', self.name + ',' + str(tagId), 1)  # ReadTag
        start = time.time()
        counter = 0
        while self.msg == 'get':
            if time.time() - start > self.retrySendingAfterSeconds:
                if counter >= self.maxAmountRetriesSending:
                    return 'took too long try sending new tag'
                print('retry sending ReadTag')
                self.sendPublish('RT', self.name + ',' + str(tagId), 1)  # ReadTag
                counter += 1
                start = time.time()
        return self.msg
