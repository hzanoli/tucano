![Image of a tucano](https://github.com/hzanoli/tucano/docs/images/tucano.svg)
# tucano

Tucano will help you to set up and run singularity containers in HPC clusters. 


# Introduction 
Tucano helps you organize your workflow when using containers in High Performance Computers (HPC). 

You should be guided by the following philosophy:

- Create a container image with all the software dependencies you need. 

- Upload the container image to docker hub.

- Use `tucano init` to generate a configuration file. Replace the value of `image` 
  to the one corresponding to your image on docker hub. 
  
- Include any directories you will need in the configuration file, under `volumes`. A 
  few directories are already available in by default, and you do not need to add them:
  your home folder, a directory called `workspace` in the same directory as the configuration
  file, and the necessary directories to forward your X11 session.
  
After that, you can use `tucano shell` to open a shell inside the container for you or
`tucano run` to run a single command inside your container.

This documentation will be expanded with more detailed used cases and examples.