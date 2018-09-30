# weather

A little container to get weather data from api.openweathermap.org

### Getting an API key

To get an API key for this app you need to visit

> https://home.openweathermap.org/users/sign_up

Using the free account is sufficiant to make this app work

Once you have signed up your key will be at

> https://home.openweathermap.org/api_keys

### Building the container

From the dir with the Dockerfile in run

> docker build -t sdwenham/weather .

### Runing from docker

> docker run -e OPENWEATHERMAP_KEY={api-key} sdwenham/weather {city} 
