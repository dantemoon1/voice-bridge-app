<script lang="ts">
  import { onMount } from 'svelte';

  let socket: WebSocket;
  let mediaRecorder: MediaRecorder;

  async function startStreaming() {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    socket = new WebSocket('ws://localhost:8000/ws/stream');
    
    mediaRecorder = new MediaRecorder(stream);
    mediaRecorder.ondataavailable = (event) => {
      if (event.data.size > 0 && socket.readyState === WebSocket.OPEN) {
        socket.send(event.data);
      }
    };
    mediaRecorder.start(100); // 100ms chunks
  }

  onMount(() => {
    // Microphone permission handled by Capacitor/iOS
  });
</script>

<main>
  <h1>Voice Bridge</h1>
  <button on:click={startStreaming}>Start Voice Stream</button>
</main>

<style>
  main { text-align: center; padding: 2em; }
  button { padding: 1em 2em; font-size: 1.2em; }
</style>
