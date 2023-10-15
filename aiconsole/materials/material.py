from enum import Enum
from pydantic import BaseModel
from aiconsole.materials.documentation_from_code import documentation_from_code
from aiconsole.materials.rendered_material import RenderedMaterial
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from aiconsole.materials.content_evaluation_context import ContentEvaluationContext

class MaterialStatus(str, Enum):
    DISABLED = "disabled"
    ENABLED = "enabled"
    FORCED = "forced"

class MaterialContentType(str, Enum):
    STATIC_TEXT = "static_text"
    DYNAMIC_TEXT = "dynamic_text"
    API = "api"

class MaterialLocation(str, Enum):
    AICONSOLE_CORE = "aiconsole"
    PROJECT_DIR = "project"

class Material(BaseModel):
    id: str
    usage: str
    defined_in: MaterialLocation
    status: MaterialStatus = MaterialStatus.ENABLED
    
    # Content, either static or dynamic
    content_type: MaterialContentType = MaterialContentType.STATIC_TEXT
    content_static_text: str = """

# Header

content, content content

## Sub header

Bullets in sub header:
* Bullet 1
* Bullet 2
* Bullet 3

""".strip()
    content_dynamic_text: str = """

import random
    
def content(context):
    samples = ['sample 1' , 'sample 2', 'sample 3', 'sample 4']
    return f'''
# Examples of great content
{random.sample(samples, 2)}

'''.strip()

""".strip()
    content_api: str = """

'''
General API description
'''

def create():
    '''
    Use this function to print 'Created'
    '''
    print "Created"

def list()
    '''
    Use this function to print 'list'
    '''
    print "List"

""".strip()

    async def content(self, context: 'ContentEvaluationContext') -> str:
        if self.content_type == MaterialContentType.DYNAMIC_TEXT:
            try:
                # Try compiling the python code and run it
                source_code = compile(self.content_dynamic_text, '<string>', 'exec')
                local_vars = {}
                exec(source_code, local_vars)
                content_func = local_vars.get('content')
                if callable(content_func):
                    return content_func(context)
                else:
                    raise Exception('No callable content function found!')
            except Exception as e:
                # If there is any error while compiling or running the code, return an empty string
                # and add log (or notify about error).
                raise Exception(f'Error in content source: {e}')
        elif self.content_type == MaterialContentType.STATIC_TEXT:
            return self.content_static_text
        elif self.content_type == MaterialContentType.API:
            return documentation_from_code(self.content_api)(context)
        else:
            raise ValueError("Material has no content")
        
    async def render(self, context: 'ContentEvaluationContext'):
        content = await self.content(context)
        return RenderedMaterial(id=self.id, content=content)
