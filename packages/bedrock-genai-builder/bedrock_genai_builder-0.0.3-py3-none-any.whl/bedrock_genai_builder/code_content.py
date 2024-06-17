code_structure_list = [
    {
        "code": """from bedrock_util.bedrock_genai_util.TextCompletionUtil import generate_text_completion
from bedrock_util.bedrock_genai_util.prompt_service import run_service
from bedrock_util.bedrock_genai_util.agent_service import run_agent
import boto3

bedrock_client = boto3.client(service_name='bedrock-runtime')

def lambda_handler(event, context):
    \"""
    If we want to directly use the FM API , use - generate_text_completion
    
    If we want to use prompt service framework - run_service 
    
    If we want to use agent service - run_agent
 

    \"""



    return {
        'statusCode': 200,
        'body': 'Hello from Lambda!'
    }""",
        "file_name": "lambda_function.py",
    },
    {
        "code": """from bedrock_util.bedrock_genai_util.TextCompletionUtil import generate_text_completion
from bedrock_util.bedrock_genai_util.prompt_service import run_service
from bedrock_util.bedrock_genai_util.agent_service import run_agent
import boto3

bedrock_client = boto3.client(service_name='bedrock-runtime')

\"""
    This block of code demonstrates how to invoke methods for generating text completions
    and running a prompt service flow based on service ID which it verifies from prompt_store.yaml file.


    example:

    If we want to directly use the FM API , use - generate_text_completion

    If we want to use prompt service framework - run_service 

\"""
""",
        "file_name": "bedrock_app.py",
    },
    {
        "code": """##############################################################################################
#   Create YAML file content for prompt service flow. Example:                               #
#                                                                                            #
#  PromptServices:                                                                           #
#                                                                                            #
#    getMathDetails:                                                                         #
#      prompt: |                                                                             #
#        You are an expert math teacher. Based on user input below provide assistance.       #
#                                                                                            #
#        input: {input}                                                                      #
#      inputVariables:                                                                       #
#        - input                                                                             # 
#      guardrailIdentifier: "test"                                                             #
#      guardrailVersion:"1"                                                                    #
#      allowedFoundationModelProviders:                                                      #
#        - Amazon                                                                            #
#        - Meta                                                                              #
#        - Anthropic                                                                         #
#        - Mistral AI                                                                        #
#        - Cohere                                                                            #
##############################################################################################""",
        "file_name": "prompt_store.yaml",
    },
    {
        "code": """###############################################################################
# Create YAML content for agent service as per below format-
#
# AgentServices:
#   <agent service id>:
#     agentInstruction: |
#       <Agent instruction>
#     allowedTools:
#       - <list of functions to be used as tools>
#
# e.g-
#
# AgentServices:
#   mathService:
#     agentInstruction: |
#       You are an expert math teacher. Based on user input provide assistance.
#     allowedTools:
#       - sum
###############################################################################

###############################################################################
# Key                | Description
###############################################################################
# AgentServices      | This is the root key for the YAML file. It contains
#                    | one or more agent services.
###############################################################################
# <agent service id> | This is the key for a specific agent service. It is
#                    | used to identify and reference the service.
###############################################################################
# agentInstruction   | This is the instruction or description for the agent
#                    | service. It can be a multi-line string using the pipe
#                    | (|) character.
###############################################################################
# allowedTools       | This is the list of allowed tools (functions) for the
#                    | agent service. Each function is listed as an item in the
#                    | list.
###############################################################################""",
        "file_name": "agent_store.yaml",
    },
    {
        "code": """{
  "agentFunctions": {
  }
}""",
        "file_name": "tool_spec.json",
    },
]
