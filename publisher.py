#!/usr/bin/env python
# ------------------------------------------------------------------------
# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
# 
# http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ------------------------------------------------------------------------
 
import time
import sys
import os
import stomp

user = os.getenv("ACTIVEMQ_USER") or "admin"
password = os.getenv("ACTIVEMQ_PASSWORD") or "password"
host = os.getenv("ACTIVEMQ_HOST") or "localhost"
port = os.getenv("ACTIVEMQ_PORT") or 61613
#destination = sys.argv[1:2] or ["/topic/event"]
#destination = destination[0]

data = "Hello World from Python"

#conn = stomp.Connection(host_and_ports = [(host, port)])
conn = stomp.Connection(host_and_ports = [("35.9.22.201", port)])
#conn = stomp.Connection(host_and_ports = [("10.0.1.17", port)])
conn.start()
conn.connect(login=user,passcode=password)

conn.send(body=' '.join(sys.argv[1:]), destination='TEST.FOO')
  #conn.send(data, destination=destination, persistent='false')
  
#conn.send(body="SHUTDOWN", destination='/queue/test2')

conn.disconnect()