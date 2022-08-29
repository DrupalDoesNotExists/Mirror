# Mirror - New way to access your APIs

Sometimes, the developer has to keep track of changes in the API. But, if the API is based on HTTPS, it turns into many lines of code.

There is a Mirror specifically for this. It does this for you in an elegant, fast and practical way and allows you to work based on the PubSub pattern.

## How it works?

Mirror works on the basis of "rays". When one of the clients subscribes, a "ray" is created for it in redis. On each update, Mirror compares the ray's previous state with the current state, and if they differ, subscribers will receive an event.

## Installation

You can deploy Mirror as default flask application with Gunicorn/Nginx/UWSGI or use dev server.

You can confirm successfull installation by requesting root. It should return 418 code.

## Original Usage

Mirror was originally designed to work with the Hypixel API and track player-related events.

## Contributions

All stuff licensed under MIT. Any contributions are welcome.
Use PRs to apply your changes!
