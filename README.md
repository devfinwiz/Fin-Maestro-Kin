<p align="center">
  <a href="https://fin-maestro-kin.apidog.io/"><img src="https://github.com/devfinwiz/Fin-Maestro-Kin/assets/78873223/eb0f030e-5c6c-4457-9713-97d0487ae59c" alt="Fin Maestro Kin"></a>
</p>
<p align="center" style="font-size: 20px;">
    <em>Seamless Finance: Docker-Deployed APIs for Smart Investments.</em>

<h1 align="center">Fin-Maestro-Kin </h1>

<p align="center">
  <a href="https://github.com/devfinwiz/fin-maestro-kin/releases/latest">
    <img src="https://img.shields.io/github/v/release/devfinwiz/fin-maestro-kin?style=for-the-badge">
  </a>
  <a href="">
    <img src="https://img.shields.io/badge/Python-3.9.1-blue&?style=for-the-badge&color=brown">
  </a>
  <a href="https://github.com/devfinwiz/Fin-Maestro-Kin/blob/master/LICENSE">
    <img src="https://img.shields.io/github/license/devfinwiz/Fin-Maestro-Kin?color=purple&style=for-the-badge">
  </a>
  <a href="https://github.com/devfinwiz/Fin-Maestro-Kin/graphs/contributors">
    <img src="https://img.shields.io/github/contributors/devfinwiz/Fin-Maestro-Kin?color=indigo&style=for-the-badge">
  </a>
  <a href="https://www.codefactor.io/repository/github/devfinwiz/fin-maestro-kin">
    <img src="https://www.codefactor.io/repository/github/devfinwiz/fin-maestro-kin/badge?style=for-the-badge&">
  </a>
  <a href="https://hub.docker.com/repository/docker/devfinwiz24/fin-maestro-kin/tags">
    <img src="https://img.shields.io/docker/pulls/devfinwiz24/fin-maestro-kin?style=for-the-badge&logo=docker">
  </a>
</p><br>


| **Docker** | **Discussion** | **Bugs/Issues** | **Contribute** |
| :---: | :---: | :---: | :---: |
| [![Use](https://github.com/devfinwiz/Fin-Maestro-Kin/assets/78873223/5866ef40-3168-415b-b222-febb280f0248)](https://hub.docker.com/r/devfinwiz24/fin-maestro-kin) | [![meeting](https://user-images.githubusercontent.com/6128978/149935812-31266023-cc5b-4c98-a416-1d4cf8800c0c.png)](https://github.com/devfinwiz/Fin-Maestro-Kin/discussions) | [![warning](https://user-images.githubusercontent.com/6128978/149936142-04d7cf1c-5bc5-45c1-a8e4-015454a2de48.png)](https://github.com/devfinwiz/Fin-Maestro-Kin/issues/new/choose) | [![meeting](https://user-images.githubusercontent.com/6128978/149935812-31266023-cc5b-4c98-a416-1d4cf8800c0c.png)](https://github.com/devfinwiz/Fin-Maestro-Kin/fork) |
| Get started quickly using Docker | Join/Read the Community Discussion | Raise an Issue about a Problem | Contribute With New Features |


## **Fin-Maestro-Kin** empowers you to:

- 📊**Effortlessly Fetch Historical Data:** Seamlessly fetch historical financial data for in-depth analysis and market trend identification.

- 📈**Perform Market Trend Analysis:** Uncover valuable insights and identify market trends with ease, guiding your investment decisions.
  
- 📉**Evaluate Market Sentiment:** Gauge market sentiment to make informed investment decisions based on current market psychology.
  
- ⚡**Experience Lightning-Fast Performance:** Benefit from the performance and scalability of FastAPI for a seamless user experience.
  
- 🔍**Craft Unparalleled Market Insights:** Build your own financial applications powered by Fin-Maestro-Kin, unlocking a deeper understanding of the market.


![](https://i.imgur.com/waxVImv.png)

# Running Fin-Maestro-Kin in a Docker Container

## Manually with Docker Command Line Interface (CLI)

1. **Pull the Docker Image:** First, pull the pre-built Docker image from Docker Hub using the following command in your terminal or command prompt:
```
docker pull devfinwiz24/fin-maestro-kin:latest
```
2. **Run the Docker Container:** After pulling the image, run the Docker container using the following command:
```
docker run -d -p 8000:8000 -p 6379:6379 -v redis-cache:/redis-cache devfinwiz24/fin-maestro-kin:latest
```
This command pulls the latest version of the Docker image from Docker Hub and runs it in a detached mode (`-d`) while mapping port 8000 of the host machine to port 8000 of the container (`-p 8000:8000`).

## Using Docker Desktop (Optional)
> [!IMPORTANT]
> ### Prerequisite: [Download Docker Desktop](https://www.docker.com/products/docker-desktop/)

1. **Pull the Docker Image:**
   - Open Docker Desktop and navigate to the "Images" section.
   - Search for the pre-built Docker image named `devfinwiz24/fin-maestro-kin:latest`.
   - Click on the image and select "Pull" to download it to your local machine.

2. **Run the Docker Container:**
   - Once the image is pulled, navigate to the "Containers/Apps" section in Docker Desktop.
   - Click on "Run" and configure the container settings:
     - Container name (optional).
     - Port mapping: Expose port 8000 for accessing the application and port 6379 for Redis caching.
     - Volume mapping: Create a volume named "redis-cache" and mount it to the "/redis-cache" directory in the container.
   - Start the container to launch the application.

3. **Access the Application:**
   - After the Docker container is running, access the application by opening a web browser.
   - Enter http://localhost:8000/docs in the address bar to access the Fin-Maestro-Kin API documentation.

4. **Additional Docker Desktop Features:**
   - Docker Desktop provides a user-friendly graphical interface for managing Docker containers.
   - You can monitor container status, view container logs, and interact with running containers using the Docker Desktop GUI.

## Usage
After deploying the container, interact with Fin Maestro Kin by sending HTTP requests to the exposed endpoints. Refer to the API [documentation](https://fin-maestro-kin.apidog.io/) for detailed information on available endpoints and request formats.
