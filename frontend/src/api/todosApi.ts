import axios from 'axios';
import type { Todo, TodoCreate, TodoUpdate } from '../types/todo';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1',
});

export async function fetchTodos(): Promise<Todo[]> {
  const response = await api.get<Todo[]>('/todos');
  return response.data;
}

export async function fetchTodo(id: number): Promise<Todo> {
  const response = await api.get<Todo>(`/todos/${id}`);
  return response.data;
}

export async function createTodo(data: TodoCreate): Promise<Todo> {
  const response = await api.post<Todo>('/todos', data);
  return response.data;
}

export async function updateTodo(id: number, data: TodoUpdate): Promise<Todo> {
  const response = await api.put<Todo>(`/todos/${id}`, data);
  return response.data;
}

export async function deleteTodo(id: number): Promise<void> {
  await api.delete(`/todos/${id}`);
}

export async function completeTodo(id: number): Promise<Todo> {
  const response = await api.patch<Todo>(`/todos/${id}/complete`);
  return response.data;
}

export async function uncompleteTodo(id: number): Promise<Todo> {
  const response = await api.patch<Todo>(`/todos/${id}/uncomplete`);
  return response.data;
}
