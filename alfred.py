import requests
import openai
import spacy

openai.api_key = "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"
client = openai.OpenAI()

nlp = spacy.load("en_core_web_sm")

def get_weather(loc): # get weather data from OpenWeatherMap
    weather_api_key = "57e390f9102ded21a4ddc8d410d507e7"
    complete = "http://api.openweathermap.org/data/2.5/weather?q=" + loc + "&appid=" + weather_api_key + "&units=metric"

    response = requests.get(complete)
    weather_data = response.json()

    if weather_data['cod'] != 200:
        print("I'm afraid I couldn't fetch the weather data, sir.")
        return None
    
    main_data = weather_data["main"]
    weather = weather_data["weather"][0]
    wind = weather_data["wind"]

    return {"temperature": main_data["temp"], "feels_like": main_data["feels_like"], "description": weather["description"], "wind_speed": wind["speed"], "humidity": main_data["humidity"]}

def extract_location(input): # find location from user prompt
    doc = nlp(input)
    for entity in doc.ents:
        if entity.label_ == "GPE":
            return entity.text
            
def remove_location(input, location): # isolates context of user's activities by removing location from the input
    return input.replace(location, "")

def alfred_response(input):
    if input.lower() in ["exit", "quit"]:
        prompt_tip = "You are Alfred, Batman's butler. Bruce Wayne said that he would like to end the conversation. Respond in Alfred's formal, well-spoken, and concise style by politely closing the conversation and offering Master Wayne ongoing assistance whenever needed."
        completion = client.chat.completions.create(
            model = "gpt-3.5-turbo",
            messages = [
                {"role": "system", "content": prompt_tip},
                {"role": "user", "content": input}
            ]
        )
        return "Alfred: " + completion.choices[0].message.content
    
    location = extract_location(input)

    if not location:
        prompt_tip = "You are Alfred, Batman's butler. Bruce Wayne has given you an invalid or an unclear location. Respond in Alfred's formal, well-spoken, and concise style by stating that you could not recognize that location and politely asking Master Wayne to provide another one."
        completion = client.chat.completions.create(
            model = "gpt-3.5-turbo",
            messages = [
                {"role": "system", "content": prompt_tip},
                {"role": "user", "content": input}
            ]
        )
        return "Alfred: " + completion.choices[0].message.content
    
    context = remove_location(input, location)
    weather = get_weather(location)

    temperature, feels_like, description, wind_speed, humidity = weather["temperature"], weather["feels_like"], weather["description"], weather["wind_speed"], weather["humidity"]
    prompt_tip = "You are Alfred, Batman's butler. Bruce Wayne is asking for advice on what to wear today. The weather in " + str(location) + " is " + str(description) + " with a temperature of " + str(temperature) + " C, though it feels like " + str(feels_like) + " C. The wind speed is " + str(wind_speed) + " m/s and the humidity is " + str(humidity) + "%. Bruce Wayne is planning to " + str(context) + ". Respond in Alfred's formal, well-spoken, and concise style and give an outfit recommendation. Make sure you include the actual statistics of the weather. Do not include a closing remark or signature in your response. Include a follow-up question asking if further assistance is required."
    completion = client.chat.completions.create(
        model = "gpt-3.5-turbo",
        messages = [
            {"role": "system", "content": prompt_tip},
            {"role": "user", "content": input}
        ]
    )
    return "Alfred: " + completion.choices[0].message.content

def main():
    print("Alfred: Good day, Master Wayne. How may I assist you today?")
    user_in = input("User (type exit or quit to end conversation): ")
    while user_in not in ["exit", "quit"]:
        print(alfred_response(user_in))
        user_in = input("User (type exit or quit to end conversation): ")
        print()
        if user_in in ["exit", "quit"]:
            print(alfred_response(user_in))
            break
    

if __name__ == "__main__":
    main()