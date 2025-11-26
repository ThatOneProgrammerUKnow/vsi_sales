

# Contributing
## Dev Setup
### Database
It is highly recommend that you run your database in a docker container. See the [postgres](https://hub.docker.com/_/postgres)


```shell
> docker run -d --name postgres -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=healthy_herbs -e POSTGRES_USER=postgres

# Confirm the container is running. You should see a "postgres" container if you run
> docker ps
```

### Environment variables
Environment variables are read from the `.env` file. Copy the `.env.example` file.
```shell
> cp .env.example .env
```

### Python setup
We use the [uv](https://docs.astral.sh/uv/guides/install-python/) tool to manage python dependencies. As always, use a virtual environment for your python dependencies. uv makes it easy to set up everything.

```shell
> uv venv
> source .venv/bin/activate
> uv sync
```

### Styles
For styles, we use the [tailwind css](https://tailwindcss.com/docs/installation/using-vite) framework and the [DaisyUI](https://daisyui.com/components/) framework that is built with Tailwind. Prefer getting things done with DaisyUI and tailwind. It just makes everything easier in the long run.

#### Install everything
```shell
> npm install
```

Styles are bundled with webpack. This means that we need to recompile the bundles often. There is an npm script that should take care of this by auto-bundling everything. In a separate terminal window, run

```shell
> npm run dev-watch
```


### Running the server
Before running the server, first run all migrations
```shell
python manage.py migrate
```

Now you can run the django development server:
```shell
python manage.py runserver
```

## Creating new Django apps
- in the apps directory, create a folder with your app's name
- run
```shell
python .\manage.py startapp {your-app-name} apps/{your-app-name}
```