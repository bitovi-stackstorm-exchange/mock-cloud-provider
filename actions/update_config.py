import sys
import json

from st2common.runners.base_action import Action
from st2client.client import Client
from st2client.models import KeyValuePair

class UpdateConfigAction(Action):
    def run(self, key_name, server_id, action, server_state):
      self.client = Client(base_url='http://localhost')

      servers_object = {}

      # if key_name exists, use it
      servers_json = self.client.keys.get_by_name(name=key_name)
      if servers_json:
        servers_object = json.loads(servers_json.value)


      if action == "delete":
        del servers_object[server_id]
      else:
        server_object = servers_object.get(server_id)

        if server_object:
          server_object["server_state"] = server_state
        else:
          servers_object[server_id] = {
            "server_state": server_state
          }

      self.client.keys.update(KeyValuePair(name=key_name, value=json.dumps(servers_object)))
      return { "servers": servers_object }