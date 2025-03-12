FROM postgres:latest
ENV POSTGRES_DB=postgres_tsp_db
ENV POSTGRES_USER=postgres
ENV POSTGRES_PASSWORD=postgres
EXPOSE 5432