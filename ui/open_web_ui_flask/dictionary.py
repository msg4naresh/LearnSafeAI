from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Mock static JSON response
static_json = {
  "meanings": [
    {
      "category": "Python - Parallel Programming",
      "expertise_level": 1,
      "period": "2024-10-01",
      "recommendations": "Introduction to threading and multiprocessing."
    },
    {
      "category": "Python - Data Processing",
      "expertise_level": 1.5,
      "period": "2024-10-01",
      "recommendations": "Introduction to pandas and basic data manipulation."
    },
    {
      "category": "Java - Concurrency",
      "expertise_level": 2,
      "period": "2024-10-01",
      "recommendations": "Introduction to ExecutorService and basic threading."
    },
    {
      "category": "Python - Parallel Programming",
      "expertise_level": 2,
      "period": "2024-10-02",
      "recommendations": "Learn threading libraries and multiprocessing basics."
    },
    {
      "category": "Python - Data Processing",
      "expertise_level": 2.5,
      "period": "2024-10-02",
      "recommendations": "Learn advanced pandas operations for data handling."
    },
    {
      "category": "Java - Concurrency",
      "expertise_level": 2.7,
      "period": "2024-10-02",
      "recommendations": "Understanding thread pools and concurrency models."
    },
    {
      "category": "Python - Parallel Programming",
      "expertise_level": 3,
      "period": "2024-10-03",
      "recommendations": "Advanced multiprocessing with concurrent.futures."
    },
    {
      "category": "Python - Data Processing",
      "expertise_level": 3.5,
      "period": "2024-10-03",
      "recommendations": "Mastering pandas with vectorized operations."
    },
    {
      "category": "Java - Concurrency",
      "expertise_level": 3.8,
      "period": "2024-10-03",
      "recommendations": "Advanced thread management with ForkJoinPool."
    },
    {
      "category": "Python - Parallel Programming",
      "expertise_level": 4,
      "period": "2024-10-04",
      "recommendations": "Optimize parallel execution with joblib and Dask."
    },
    {
      "category": "Python - Data Processing",
      "expertise_level": 4.5,
      "period": "2024-10-04",
      "recommendations": "Optimizing memory usage with pandas."
    },
    {
      "category": "Java - Concurrency",
      "expertise_level": 4.7,
      "period": "2024-10-04",
      "recommendations": "Enhance performance using CompletableFuture."
    },
    {
      "category": "Python - Parallel Programming",
      "expertise_level": 5,
      "period": "2024-10-05",
      "recommendations": "Expert-level parallel programming using Ray."
    },
    {
      "category": "Python - Data Processing",
      "expertise_level": 5.5,
      "period": "2024-10-05",
      "recommendations": "Mastering large-scale data processing with Dask."
    },
    {
      "category": "Java - Concurrency",
      "expertise_level": 5.9,
      "period": "2024-10-05",
      "recommendations": "Implementing high-performance concurrent systems."
    },
    {
      "category": "Python - Parallel Programming",
      "expertise_level": 6,
      "period": "2024-10-06",
      "recommendations": "Utilizing Celery for distributed tasks."
    },
    {
      "category": "Python - Data Processing",
      "expertise_level": 6.5,
      "period": "2024-10-06",
      "recommendations": "Leverage Vaex for out-of-memory data processing."
    },
    {
      "category": "Java - Concurrency",
      "expertise_level": 6.8,
      "period": "2024-10-06",
      "recommendations": "Advanced Java concurrency with lock-free algorithms."
    },
    {
      "category": "Python - Parallel Programming",
      "expertise_level": 7,
      "period": "2024-10-07",
      "recommendations": "Combine multiprocessing with asyncio."
    },
    {
      "category": "Python - Data Processing",
      "expertise_level": 7.5,
      "period": "2024-10-07",
      "recommendations": "Optimize pandas operations with Modin."
    },
    {
      "category": "Java - Concurrency",
      "expertise_level": 7.9,
      "period": "2024-10-07",
      "recommendations": "Refine thread synchronization strategies."
    },
    {
      "category": "Python - Parallel Programming",
      "expertise_level": 8,
      "period": "2024-10-08",
      "recommendations": "Build distributed systems using Ray."
    },
    {
      "category": "Python - Data Processing",
      "expertise_level": 8.5,
      "period": "2024-10-08",
      "recommendations": "Advanced data processing using Polars."
    },
    {
      "category": "Java - Concurrency",
      "expertise_level": 8.7,
      "period": "2024-10-08",
      "recommendations": "Maximizing concurrency with reactive programming."
    },
    {
      "category": "Python - Parallel Programming",
      "expertise_level": 9,
      "period": "2024-10-09",
      "recommendations": "Develop high-performance distributed systems."
    },
    {
      "category": "Python - Data Processing",
      "expertise_level": 9.5,
      "period": "2024-10-09",
      "recommendations": "Process huge datasets efficiently using Vaex."
    },
    {
      "category": "Java - Concurrency",
      "expertise_level": 9.9,
      "period": "2024-10-09",
      "recommendations": "Master lock-free data structures."
    },
    {
      "category": "Python - Parallel Programming",
      "expertise_level": 10,
      "period": "2024-10-10",
      "recommendations": "Optimize parallel workloads with Ray and Dask."
    },
    {
      "category": "Python - Data Processing",
      "expertise_level": 10,
      "period": "2024-10-10",
      "recommendations": "Leverage cutting-edge tools for large-scale data analysis."
    },
    {
      "category": "Java - Concurrency",
      "expertise_level": 10,
      "period": "2024-10-10",
      "recommendations": "Achieve peak performance with asynchronous systems."
    }
  ]
}


@app.route('/meaning', methods=['GET'])
def get_meaning():
    # Get the flag from query parameters (e.g., /meaning?flag=dynamic)
    flag = request.args.get('flag', 'static')

    if flag == 'dynamic':
        # You can add dynamic logic here
        dynamic_json = {
            "meanings": [
                {
                    "activity": "Python",
                    "category": "machine-learning",
                    "recommendations": "Dynamic: Use TensorFlow for ML.",
                    "period": "2024-05"
                },
                {
                    "activity": "Java",
                    "category": "microservices",
                    "recommendations": "Dynamic: Use Spring Boot for microservices.",
                    "period": "2024-06"
                }
            ]
        }
        return jsonify(dynamic_json)

    return jsonify(static_json)

if __name__ == '__main__':
    app.run(debug=True)
