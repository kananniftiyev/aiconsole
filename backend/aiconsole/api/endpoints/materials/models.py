# The AIConsole Project
#
# Copyright 2023 10Clouds
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from sqlalchemy import Column, Integer, String, Text, Enum, ARRAY, BOOLEAN
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

class Material(Base):
    __tablename__ = 'materials'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    version = Column(String)
    usage = Column(Text)
    usage_examples = Column(ARRAY(Text))
    defined_in = Column(String)  # New field
    type = Column(String)  # New field
    default_status = Column(String)
    status = Column(String)  # New field
    override = Column(BOOLEAN)  # New field
    content_type = Column(Enum('api', 'dynamic_text', 'static_text', name='materialcontenttype'))
    content = Column(Text)
    content_static_text = Column(Text)
    default_status = Column(String)
