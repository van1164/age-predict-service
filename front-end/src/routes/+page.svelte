<script>
	import {Dropzone, P, Button, Heading} from 'flowbite-svelte'
  import axios from 'axios'
  let value = null
	let loading = false
	let image = null
  let file = null;
  let age = null
	
  const reset = () =>{
    location.href = "/"
  }
  
    const dropHandle = (event) => {
    value = [];
    event.preventDefault();
    if (event.dataTransfer.items) {
      [...event.dataTransfer.items].forEach((item, i) => {
        if (item.kind === 'file') {
          const file = item.getAsFile();
          value.push(file);
          value = value;
        }
      });
    } else {
      [...event.dataTransfer.files].forEach((file, i) => {
        value = file;
      });
    }
  };

  const handleChange = (event) => {
	const input = event.target;
  console.log(input)
	if (input.files) {
		file = input.files[0];
	}
	const reader = new FileReader();
	reader.onload = function (event) {
		image = event.target?.result;
	}
	if (input) {
		reader.readAsDataURL(file);
	}

  };

  async function send(){
    loading = true
    await axios.post("http://localhost/upload",{
        file
      },
      {
        headers:{"content-type": "multipart/form-data"},
      }).then(
        response => {
          console.log(response.data.age)
          age = response.data.age
        }
      )
  }

</script>

<svelte:head>
	<title>Face AI</title>
</svelte:head>

<section>
  <form on:submit|preventDefault={send}>
	<div class= "mb-3">
		<P class="text-3xl xs:text-5xl sm:text-5xl base:text-7xl md:text-5xl lg:text-5xl xl:text-5xl 2xl:text-7xl font-extrabold text-center">얼굴 나이를 예측해드려요</P>
	</div>
    {#if image == null}
    <Dropzone
    id="dropzone"
    on:drop={dropHandle}
    on:dragover={(event) => {
      event.preventDefault();
    }}
    on:change={handleChange}
    defaultClass="flex flex-col justify-center items-center w-full h-96 bg-gray-50 rounded-lg border-2 border-gray-300 border-dashed cursor-pointer dark:hover:bg-bray-800 dark:bg-gray-700 hover:bg-gray-100 dark:border-gray-600 dark:hover:border-gray-500 dark:hover:bg-gray-600"
    required
    >
    <svg aria-hidden="true" class="mb-3 w-10 h-10 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" /></svg>

      <p class="mb-2 text-sm text-gray-500 dark:text-gray-400"><span class="font-semibold">Click to upload</span> or drag and drop</p>
      <p class="text-xs text-gray-500 dark:text-gray-400">PNG,JPG</p>
  </Dropzone>
  {:else}
  {#key image}
  <div class="w-full content-center m-auto">
  <img class=" sm:w-56 md:w-72 lg:w-80 xl:w-96 2xl:w-96 m-auto" src={image} alt="Preview" />
</div>
  {/key}
	{/if}
  {#key loading}
  {#key age}
  {#if age !=null}
  <Button class = "mt-5 mb-5 h-30 w-full" on:click={reset}>다시하기</Button>
  {:else if loading == true}
  <Button color = blue class = "mt-5 mb-5 h-30 w-full" type="submit" disabled >업로드중.....</Button>
  {:else if file == null}
  <Button color = blue class = "mt-5 mb-5 h-30 w-full" type="submit" disabled>업로드</Button>
  {:else}
  <Button color = blue class = "mt-5 mb-5 h-30 w-full" type="submit">업로드</Button>
  {/if}
{/key}
{/key}
</form>
{#key age}
  {#if age !=null}
  <P>당신의 얼굴나이는 {age}살 입니다.</P>
  {/if}
{/key}
</section>


<style>
	section {
		display: flex;
		flex-direction: column;
		justify-content: center;
		align-items: center;
		flex: 0.6;
	}

</style>
