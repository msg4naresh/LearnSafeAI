<script>
  import { onMount, afterUpdate } from 'svelte';
  import { getMeaning } from '$lib/apis/chats'; // Replace this with your actual API function
  import Chart from 'chart.js/auto'; // Chart.js for rendering graphs

  let searchResults = [];
  let activeTab = 'list'; // Track active tab (default to 'list')
  let chartData = {}; // Data for the chart
  let chartInstance;

  // A map that will hold dynamic category-to-numeric mapping
  let categoryMap = {};
  let categoryLabels = []; // Holds the unique categories for display on the Y-axis

  // Fetch data on page load
  onMount(async () => {
    try {
      const response = await getMeaning(); // Fetch the data from the API

      console.log("API Response:", response); // Debugging API response
      
      if (response.meanings && Array.isArray(response.meanings)) {
        searchResults = response.meanings; // Store the data in searchResults

        // Prepare chart data (for the chart tab)
        chartData = prepareChartData(searchResults);
      } else {
        console.error("No meanings found or invalid response format");
      }
    } catch (error) {
      console.error("Error fetching data:", error);
    }
  });

  // Prepare chart data for visualization
  const prepareChartData = (data) => {
    let chartData = {
      labels: [], // Period for X-axis (month-wise)
      datasets: []
    };

    const activities = {}; // Organize the data by category (activity)
    let currentCategoryIndex = 1; // Initialize category index to map categories dynamically

    // Extract all unique periods and categories
    let allPeriods = [];
    let allCategories = [];

    data.forEach((item) => {
      const { period, category } = item;

      if (!allPeriods.includes(period)) {
        allPeriods.push(period);
      }

      if (!allCategories.includes(category)) {
        allCategories.push(category);
      }
    });

    // Sort the periods
    allPeriods.sort();

    // Initialize the category map dynamically
    allCategories.forEach((category) => {
      if (!categoryMap[category]) {
        categoryMap[category] = currentCategoryIndex;
        categoryLabels.push(category); // Store the category labels for display on Y-axis
        currentCategoryIndex++;
      }
    });

    // Initialize datasets for each category
    allCategories.forEach((category) => {
      activities[category] = {
        label: category,
        data: new Array(allPeriods.length).fill(null), // Initialize with null values for every period
      };
    });

    // Fill in the data based on available information
    data.forEach((item) => {
      const { category, expertise_level, period } = item;

      // Find the index of the current period
      const periodIndex = allPeriods.indexOf(period);

      // Set the expertise level in the correct position in the data array
      activities[category].data[periodIndex] = expertise_level;
    });

    // Map activities to datasets in the format expected by Chart.js
    chartData.labels = allPeriods; // X-axis will be the periods (months)
    chartData.datasets = Object.keys(activities).map((key) => ({
      label: activities[key].label,
      data: activities[key].data, // Add the expertise level data
      borderColor: getRandomColor(), // Generate random color for each dataset
      fill: false // No fill for line chart
    }));

    return chartData;
  };

  // Generate random color for chart lines
  const getRandomColor = () => {
    return `#${Math.floor(Math.random() * 16777215).toString(16)}`;
  };

  // Initialize the chart with Chart.js
  const initializeChart = () => {
    const canvas = document.getElementById('myChart');
    
    if (canvas) {
      const ctx = canvas.getContext('2d');
      if (chartInstance) {
        chartInstance.destroy(); // Destroy the previous chart if it exists
      }

      chartInstance = new Chart(ctx, {
        type: 'line', // Line chart
        data: chartData,
        options: {
          scales: {
            x: {
              title: {
                display: true,
                text: 'Period (month-wise)' // X-axis label
              }
            },
            y: {
              title: {
                display: true,
                text: 'Category' // Y-axis label
              },
              ticks: {
                callback: function(value) {
                  // Convert numeric value back to category label dynamically
                  return categoryLabels[value - 1]; // Map numeric value to category label
                }
              }
            }
          }
        }
      });
    } else {
      console.error("Canvas element not found");
    }
  };

  const switchTab = (tabName) => {
    activeTab = tabName;
  };

  // Ensure chart is initialized after the DOM has updated
  afterUpdate(() => {
    if (activeTab === 'chart') {
      initializeChart(); // Initialize the chart when switching to the chart tab
    }
  });
</script>

<svelte:head>
  <title>Activity History & Expertise Chart</title>
</svelte:head>

<div class="px-4 py-2">
  <div class="tabs">
    <button on:click={() => switchTab('list')} class:active={activeTab === 'list'}>List View</button>
    <button on:click={() => switchTab('chart')} class:active={activeTab === 'chart'}>Chart View</button>
  </div>

  {#if activeTab === 'list'}
    <h1 class="text-xl font-semibold">Activity History</h1>
    {#if searchResults.length > 0}
      <!-- Table for displaying activity history -->
      <table class="table-auto w-full border-collapse border border-gray-300 mt-4">
        <thead>
          <tr>
            <th class="border border-gray-300 px-4 py-2">Category</th>
            <th class="border border-gray-300 px-4 py-2">Expertise Level</th>
            <th class="border border-gray-300 px-4 py-2">Recommendations</th>
            <th class="border border-gray-300 px-4 py-2">Period</th>
          </tr>
        </thead>
        <tbody>
          {#each searchResults as result}
            <tr>
              <td class="border border-gray-300 px-4 py-2">{result.category}</td>
              <td class="border border-gray-300 px-4 py-2">{result.expertise_level}</td>
              <td class="border border-gray-300 px-4 py-2">{result.recommendations}</td>
              <td class="border border-gray-300 px-4 py-2">{result.period}</td>
            </tr>
          {/each}
        </tbody>
      </table>
    {:else}
      <p>No activity history found.</p>
    {/if}
  {/if}

  {#if activeTab === 'chart'}
    <h1 class="text-xl font-semibold">Expertise Level Over Time</h1>
    <canvas id="myChart" width="400" height="200"></canvas>
  {/if}
</div>

<style>
  .tabs {
    display: flex;
    gap: 1rem;
  }
  button {
    padding: 0.5rem 1rem;
    cursor: pointer;
    border: 1px solid #ccc;
  }
  button.active {
    background-color: #007bff;
    color: white;
  }
  table {
    width: 100%;
    border-collapse: collapse;
  }
  th, td {
    padding: 8px;
    text-align: left;
  }
  th {
    background-color: #f2f2f2;
  }
</style>
