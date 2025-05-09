import os
from dotenv import load_dotenv
import yaml
from openai import OpenAI
import json
from datetime import datetime

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API")

client = OpenAI(api_key=OPENAI_API_KEY)

def load_generate_associations_prompt_template(topic=None):
    with open("HUMORS/generate_associations_prompts.yaml", "r", encoding="utf-8") as f:
        generate_associations_prompts = yaml.safe_load(f)
    return generate_associations_prompts

def load_expand_associations_prompt_template(topic=None, associations=None):
    with open("HUMORS/expand_associations_prompts.yaml", "r", encoding="utf-8") as f:
        expand_associations_prompts = yaml.safe_load(f)
    return expand_associations_prompts

def load_refine_and_combine_associations_prompt_template(topic=None, associations=None, expanded_associations=None):
    with open("HUMORS/refine_and_combine_associations.yaml", "r", encoding="utf-8") as f:
        refine_and_combine_associations_prompts = yaml.safe_load(f)
    return refine_and_combine_associations_prompts

def load_generate_jokes_prompt_template(topic=None, associations=None, expanded_associations=None, refined_associations=None):
    with open("HUMORS/generate_jokes_prompts.yaml", "r", encoding="utf-8") as f:
        generate_jokes_prompts = yaml.safe_load(f)
    return generate_jokes_prompts

def get_input():
    topic = input("Enter a topic: ")
    return topic

def generate_associations(topic):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that generates associations for a given topic."},
            {"role": "user", "content": f"Generate associations for the topic: {topic}"}
        ]
    )

    return response.choices[0].message.content

def expand_associations(topic, associations):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that expands associations for a given topic."},
            {"role": "user", "content": f"Expand associations for the topic: {topic}"}
        ]
    )

    return response.choices[0].message.content

def refine_and_combine_associations(topic, associations, expanded_associations):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that refines and combines associations for a given topic."},
            {"role": "user", "content": f"Refine and combine associations for the topic: {topic}"}
        ]
    )

    return response.choices[0].message.content

def generate_jokes(topic, associations, expanded_associations, refined_associations):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that generates jokes for a given topic."},
            {"role": "user", "content": f"Generate jokes for the topic: {topic}"}
        ]
    )

    return response.choices[0].message.content

def save_response(response_data, step_name, topic):
    # 결과를 저장할 디렉토리 생성
    output_dir = "outputs"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # 파일명에 timestamp 추가하여 저장
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{output_dir}/{topic}_{step_name}_{timestamp}.json"
    
    with open(filename, "w", encoding="utf-8") as f:
        json.dump({"topic": topic, "response": response_data}, f, ensure_ascii=False, indent=2)
    
    return filename

def save_markdown(response_data, topic):
    output_dir = "outputs"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{output_dir}/{topic}_jokes_{timestamp}.md"
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"# Jokes about {topic}\n\n")
        f.write(response_data)
    
    return filename

def main():
    topic = get_input()

    associations = generate_associations(topic)
    save_response(associations, "associations", topic)

    expanded_associations = expand_associations(topic, associations)
    save_response(expanded_associations, "expanded_associations", topic)

    refined_associations = refine_and_combine_associations(topic, associations, expanded_associations)
    save_response(refined_associations, "refined_associations", topic)

    jokes = generate_jokes(topic, associations, expanded_associations, refined_associations)
    save_response(jokes, "jokes", topic)
    save_markdown(jokes, topic)

    print(jokes)

if __name__ == "__main__":
    main()
