<script setup>
import { computed, onMounted, ref } from 'vue'
import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000',
})

const statuses = ['Todo', 'In Progress', 'Done']
const statusFilters = ['All', ...statuses]
const tasks = ref([])
const selectedFilter = ref('All')
const loading = ref(true)
const submitting = ref(false)
const actionError = ref('')
const loadError = ref('')
const busyTaskIds = ref(new Set())

const form = ref({
  title: '',
  description: '',
  status: 'Todo',
})

const filteredTasks = computed(() => {
  if (selectedFilter.value === 'All') return tasks.value
  return tasks.value.filter((task) => task.status === selectedFilter.value)
})

function errorMessage(error) {
  const detail = error.response?.data?.detail
  if (Array.isArray(detail)) {
    return 'Data task tidak valid. Periksa kembali judul dan status.'
  }
  if (detail === 'Task not found') return 'Task tidak ditemukan.'
  if (error.response) return 'Permintaan gagal. Periksa data task, lalu coba lagi.'
  return 'Tidak dapat terhubung ke backend. Pastikan server berjalan, lalu coba lagi.'
}

async function loadTasks() {
  loading.value = true
  loadError.value = ''
  try {
    const response = await api.get('/tasks')
    tasks.value = response.data
  } catch (error) {
    loadError.value = errorMessage(error)
  } finally {
    loading.value = false
  }
}

async function createTask() {
  actionError.value = ''
  submitting.value = true
  try {
    const response = await api.post('/tasks', {
      title: form.value.title.trim(),
      description: form.value.description.trim() || null,
      status: form.value.status,
    })
    tasks.value.push(response.data)
    form.value = { title: '', description: '', status: 'Todo' }
  } catch (error) {
    actionError.value = errorMessage(error)
  } finally {
    submitting.value = false
  }
}

function setTaskBusy(taskId, busy) {
  const next = new Set(busyTaskIds.value)
  if (busy) next.add(taskId)
  else next.delete(taskId)
  busyTaskIds.value = next
}

async function updateTaskStatus(task, event) {
  const status = event.target.value
  actionError.value = ''
  setTaskBusy(task.id, true)
  try {
    const response = await api.put(`/tasks/${task.id}`, { status })
    tasks.value = tasks.value.map((item) => item.id === task.id ? response.data : item)
  } catch (error) {
    event.target.value = task.status
    actionError.value = errorMessage(error)
  } finally {
    setTaskBusy(task.id, false)
  }
}

async function deleteTask(task) {
  actionError.value = ''
  setTaskBusy(task.id, true)
  try {
    await api.delete(`/tasks/${task.id}`)
    tasks.value = tasks.value.filter((item) => item.id !== task.id)
  } catch (error) {
    actionError.value = errorMessage(error)
  } finally {
    setTaskBusy(task.id, false)
  }
}

onMounted(loadTasks)
</script>

<template>
  <main class="page-shell">
    <header class="topbar">
      <div class="brand">
        <span class="brand-mark" aria-hidden="true">✓</span>
        <span>Alfagift Task Tracker</span>
      </div>
    </header>

    <div class="workspace">
      <section class="composer panel" aria-labelledby="new-task-heading">
        <div class="section-heading">
          <h1 id="new-task-heading">Tambah task</h1>
        </div>

        <form @submit.prevent="createTask">
          <label for="title">Judul <span class="required">*</span></label>
          <input
            id="title"
            v-model="form.title"
            type="text"
            maxlength="200"
            placeholder="Judul task"
            required
          />

          <label for="description">Deskripsi</label>
          <textarea
            id="description"
            v-model="form.description"
            rows="3"
            placeholder="Deskripsi (opsional)"
          ></textarea>

          <label for="new-status">Status</label>
          <select id="new-status" v-model="form.status">
            <option v-for="status in statuses" :key="status" :value="status">{{ status }}</option>
          </select>

          <button class="primary-button" type="submit" :disabled="submitting || !form.title.trim()">
            {{ submitting ? 'Menyimpan…' : 'Tambah task' }}
          </button>
        </form>
      </section>

      <section class="task-section" aria-labelledby="task-list-heading">
        <div class="list-heading">
          <h2 id="task-list-heading">Daftar task</h2>
          <button v-if="loadError" class="text-button" type="button" @click="loadTasks">Coba lagi</button>
        </div>

        <div class="status-filters" role="group" aria-label="Filter task berdasarkan status">
          <button
            v-for="filter in statusFilters"
            :key="filter"
            type="button"
            class="filter-button"
            :class="{ active: selectedFilter === filter }"
            :aria-pressed="selectedFilter === filter"
            @click="selectedFilter = filter"
          >{{ filter }}</button>
        </div>

        <div v-if="loading" class="state-card" role="status">
          <span>Memuat task...</span>
        </div>
        <div v-else-if="loadError" class="state-card error-state" role="alert">
          <span>{{ loadError }}</span>
        </div>
        <div v-else-if="tasks.length === 0" class="state-card empty-state">
          <strong>Belum ada task</strong>
          <span>Tambahkan task pertama.</span>
        </div>
        <div v-else-if="filteredTasks.length === 0" class="state-card empty-state">
          <span>Tidak ada task dengan status ini.</span>
        </div>
        <template v-else>
          <ul class="task-list">
            <li v-for="task in filteredTasks" :key="task.id" class="task-card">
              <div class="task-main">
                <h3>{{ task.title }}</h3>
                <p v-if="task.description" class="task-description">{{ task.description }}</p>
              </div>
              <div class="task-actions">
                <label class="visually-hidden" :for="`status-${task.id}`">Status task {{ task.title }}</label>
                <select
                  :id="`status-${task.id}`"
                  class="status-select"
                  :class="`status-${task.status.toLowerCase().replace(' ', '-')}`"
                  :value="task.status"
                  :disabled="busyTaskIds.has(task.id)"
                  @change="updateTaskStatus(task, $event)"
                >
                  <option v-for="status in statuses" :key="status" :value="status">{{ status }}</option>
                </select>
                <button
                  class="delete-button"
                  type="button"
                  :disabled="busyTaskIds.has(task.id)"
                  :aria-label="`Hapus ${task.title}`"
                  @click="deleteTask(task)"
                >
                  <span aria-hidden="true">×</span>
                  <span class="delete-label">Hapus</span>
                </button>
              </div>
            </li>
          </ul>
        </template>
      </section>
    </div>
    <p v-if="actionError" class="error-message" role="alert">{{ actionError }}</p>
  </main>
</template>
