from workers.consumer import poll_queue


# app = FastAPI()

# app.include_router(analysis.router)
# app.include_router(recommendations.router)
if __name__ == "__main__":
    print("🎯 Escutando a fila SQS...")
    poll_queue()