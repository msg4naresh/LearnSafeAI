<script>
  import { onMount } from 'svelte';
  import { history, user } from '$lib/stores';
  import { getAllChatTags, getChatListByUserId, getMeaning } from '$lib/apis/chats';

  let chats = [];
  let searchQuery = '';
  let searchResults = [];

  onMount(async () => {
    // Fetch initial chat history
    chats = await getChatListByUserId(localStorage.token, $user.id);
    history.set(chats);
  });

  const handleSearch = async () => {
    if (searchQuery.trim() !== '') {
      // Call the API to fetch search results
      const response = await getMeaning(searchQuery);

      if (response && response.meaning) {
        const meaning = response.meaning;
        let results = '';

        if (meaning.Noun) {
          results += 'Meaning (Noun):\n';
          meaning.Noun.forEach((definition) => {
            results += `- ${definition}\n`;
          });
        }

        // Add other parts of the response to the results string if needed

        searchResults = results;
      } else {
        searchResults = 'No results found.';
      }
    }
  };
</script>

<svelte:head>
  <title>History</title>
</svelte:head>

<div class="px-4 py-2">
  <h1 class="text-xl font-semibold">Meaning Search</h1>

  <div class="flex items-center mt-2">
    <input
      type="text"
      bind:value={searchQuery}
      class="w-full px-2 py-1 border border-gray-300 rounded-l"
      placeholder="Search..."
    />
    <button
      on:click={handleSearch}
      class="px-2 py-1 border border-gray-300 rounded-r"
    >
    <svg
				xmlns="http://www.w3.org/2000/svg"
				viewBox="0 0 20 20"
				fill="currentColor"
				class="w-4 h-4"
			>
				<path
					fill-rule="evenodd"
					d="M9 3.5a5.5 5.5 0 100 11 5.5 5.5 0 000-11zM2 9a7 7 0 1112.452 4.391l3.328 3.329a.75.75 0 11-1.06 1.06l-3.329-3.328A7 7 0 012 9z"
					clip-rule="evenodd"
				/>
			</svg>
    </button>
  </div>

  {#if searchResults.length > 0}
      <p class="mt-2">{searchResults}</p>
  {/if}

  <br><hr class="my-2" /><br>
  <h1 class="text-xl font-semibold">Chat history</h1>

    <table class="w-full mt-2 border-collapse">
      <thead>
        <tr>
          <th class="px-2 py-1 border border-gray-300">Title</th>
          <th class="px-2 py-1 border border-gray-300">Date</th>
        </tr>
      </thead>
      <tbody>
        {#each $history as chat (chat.id)}
          <tr>
            <td class="px-2 py-1 border border-gray-300">
              <div class="truncate">{chat.title.slice(0, 60)}...</div>
            </td>
            <td class="px-2 py-1 border border-gray-300">{chat.time_range}</td>
          </tr>
        {/each}
      </tbody>
    </table>
  
</div>