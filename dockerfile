FROM jupyter/pyspark-notebook:latest

# Set the working directory
WORKDIR /home/jovyan/app

# Copy everything into the image
COPY . /home/jovyan/app

# Fix permissions for mounted volumes — optional pre-emptive cleanup
USER root
RUN chown -R jovyan:users /home/jovyan/app && \
    mkdir -p /home/jovyan/data /home/jovyan/output && \
    chown -R jovyan:users /home/jovyan/data /home/jovyan/output

# Switch back to jovyan (safe default for Jupyter)
USER jovyan

# Launch Jupyter (or change CMD for etl_job.py if needed)
CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--NotebookApp.token=''", "--NotebookApp.password=''"]
