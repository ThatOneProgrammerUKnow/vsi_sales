# Problem Statement
ISO procedures are fundamental to WEG, ensuring consistency and quality. However, implementing and maintaining these standards require substantial time and resources. Employees responsible for compliance spend significant effort resolving errors and enforcing protocols.

One issue is user error, particularly in drive identification. Drives with similar model numbers, such as CFW701E0… and CFW700E1…, though not often, have been confused, leading to incorrect shipments. Both serial and model numbers are written or typed out at least four times for every drive.

Additionally, communication inefficiencies contribute to operational delays. Technicians must rely on emails to request drives, requiring professional formatting. Essential drive information is scattered across multiple emails, with serial numbers serving as the primary reference—a process prone to errors and inefficiencies.

Solution: The proposed program provides a centralized system for managing goods information, reducing reliance on email-based tracking. Key benefits include: • Streamlined Goods Management: Users can quickly retrieve relevant details about any item without sifting through emails or old files. • Integrated Data Entry: Information such as serial numbers—used in GRNs, Job Cards, Service reports etc.—only needs to be entered once. The system ensures consistency across all relevant documents. • Client Information Hub: Contact details for clients and responsible personnel will be stored within the program, allowing easy access to email addresses and communication records. • Enhanced Efficiency: The solution minimizes manual errors, improves workflow, and supports a more productive and reliable service.

This program will significantly optimize operations, reduce administrative workload and ensure better adherence to ISO procedures.

# Contributing
## Dev Setup
### Database
It is highly recommend that you run your database in a docker container. See the [postgres](https://hub.docker.com/_/postgres)


```shell
> docker run -d --name postgres -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=weg_solutions -e POSTGRES_USER=postgres

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