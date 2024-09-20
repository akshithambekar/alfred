# Alfred
AI chatbot with the personality of Alfred, Bruce Wayne's assistant. Provides outfit recommendations based on real-time weather data.

# Prerequisites
The following libraries must be installed:
```requests, openai, spacy```

# How it works

This chatbot uses the OpenAI API for the GPT model, OpenWeatherMap API for live weather data, and the SpaCy NLP library to differentiate the location and context in the user's input. The ```requests``` module is used to make HTTP requests.

The ```get_weather()``` method fetches data from the OpenWeatherMap API based on the location provided by the user. It returns weather information such as temperature, feels-like temperature, condition, wind speed, and humidity.

The ```extract_location()``` method returns the location provided by the user to be passed into the ```get_weather()``` method. It uses SpaCy's NLP model to identify geographic entities (GPEs, such as cities or countries) from the user's input. The ```remove_location()``` method removes the location from the user's input to provide the model with the context.

The ```alfred_response()``` handles the conversation logic. A prompt tip is given to the model with instructions on how to behave and what it should say based on the user's input. If the user inputs "exit" or "quit", Alfred sends a polite closing message. If the SpaCy model cannot find the location (either it was typed incorrectly or the model doesn't have a stored GPE for that location), Alfred responds by asking for clarification. When the user provides a location and context, weather data for that location is retrieved, incorporates the context of the user's input, and sends a request to the OpenAI APi to generate a response. Alfred then provides an outfit recommendation based on the weather and what the user is planning to do.

# How to run
On the CLI, once in the file directory, type the following command to set the API key for OpenAI:
```export OPENAI_API_KEY="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"```
This is needed to ensure that you can use the GPT model.

Then run the alfred.py file:
```python3 alfred.py```

Give Alfred a prompt with a location and context, and Alfred will reply with the weather and his outfit recommendation.
