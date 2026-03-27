import { renderHook, act, waitFor } from '@testing-library/react';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { useTodos } from './useTodos';
import type { Todo, TodoListResponse } from '../types/todo';

vi.mock('../api/todosApi');

import * as todosApi from '../api/todosApi';

const mockTodo: Todo = {
  id: 1,
  title: 'Test todo',
  description: 'A description',
  is_completed: false,
  created_at: '2026-03-25T09:00:00Z',
  updated_at: '2026-03-25T09:00:00Z',
};

const mockCompletedTodo: Todo = {
  ...mockTodo,
  is_completed: true,
};

const mockListResponse: TodoListResponse = {
  todos: [mockTodo],
  count: 1,
};

beforeEach(() => {
  vi.resetAllMocks();
});

describe('useTodos', () => {
  it('should load todos on mount and set isLoading to false', async () => {
    vi.mocked(todosApi.fetchTodos).mockResolvedValue(mockListResponse);

    const { result } = renderHook(() => useTodos());

    expect(result.current.isLoading).toBe(true);

    await waitFor(() => {
      expect(result.current.isLoading).toBe(false);
    });

    expect(result.current.todos).toEqual([mockTodo]);
    expect(result.current.error).toBeNull();
  });

  it('should set error when fetchTodos fails', async () => {
    vi.mocked(todosApi.fetchTodos).mockRejectedValue(new Error('Network error'));

    const { result } = renderHook(() => useTodos());

    await waitFor(() => {
      expect(result.current.isLoading).toBe(false);
    });

    expect(result.current.error).toBe('Network error');
    expect(result.current.todos).toEqual([]);
  });

  it('should return empty todos when API returns empty list', async () => {
    vi.mocked(todosApi.fetchTodos).mockResolvedValue({ todos: [], count: 0 });

    const { result } = renderHook(() => useTodos());

    await waitFor(() => {
      expect(result.current.isLoading).toBe(false);
    });

    expect(result.current.todos).toEqual([]);
  });

  it('should add todo to list when addTodo succeeds', async () => {
    vi.mocked(todosApi.fetchTodos).mockResolvedValue({ todos: [], count: 0 });
    vi.mocked(todosApi.createTodo).mockResolvedValue(mockTodo);

    const { result } = renderHook(() => useTodos());

    await waitFor(() => {
      expect(result.current.isLoading).toBe(false);
    });

    await act(async () => {
      await result.current.addTodo({ title: 'Test todo', description: 'A description' });
    });

    expect(result.current.todos).toHaveLength(1);
    expect(result.current.todos[0]).toEqual(mockTodo);
  });

  it('should update todo in list when editTodo succeeds', async () => {
    vi.mocked(todosApi.fetchTodos).mockResolvedValue(mockListResponse);
    const updatedTodo = { ...mockTodo, title: 'Updated' };
    vi.mocked(todosApi.updateTodo).mockResolvedValue(updatedTodo);

    const { result } = renderHook(() => useTodos());

    await waitFor(() => {
      expect(result.current.isLoading).toBe(false);
    });

    await act(async () => {
      await result.current.editTodo(1, { title: 'Updated' });
    });

    expect(result.current.todos[0]?.title).toBe('Updated');
  });

  it('should remove todo from list when removeTodo succeeds', async () => {
    vi.mocked(todosApi.fetchTodos).mockResolvedValue(mockListResponse);
    vi.mocked(todosApi.deleteTodo).mockResolvedValue(undefined);

    const { result } = renderHook(() => useTodos());

    await waitFor(() => {
      expect(result.current.isLoading).toBe(false);
    });

    await act(async () => {
      await result.current.removeTodo(1);
    });

    expect(result.current.todos).toHaveLength(0);
  });

  it('should update todo in list when toggleComplete completes a todo', async () => {
    vi.mocked(todosApi.fetchTodos).mockResolvedValue(mockListResponse);
    vi.mocked(todosApi.completeTodo).mockResolvedValue(mockCompletedTodo);

    const { result } = renderHook(() => useTodos());

    await waitFor(() => {
      expect(result.current.isLoading).toBe(false);
    });

    await act(async () => {
      await result.current.toggleComplete(mockTodo);
    });

    expect(result.current.todos[0]?.is_completed).toBe(true);
  });

  it('should update todo in list when toggleComplete uncompletes a todo', async () => {
    const completedListResponse: TodoListResponse = {
      todos: [mockCompletedTodo],
      count: 1,
    };
    vi.mocked(todosApi.fetchTodos).mockResolvedValue(completedListResponse);
    vi.mocked(todosApi.uncompleteTodo).mockResolvedValue(mockTodo);

    const { result } = renderHook(() => useTodos());

    await waitFor(() => {
      expect(result.current.isLoading).toBe(false);
    });

    await act(async () => {
      await result.current.toggleComplete(mockCompletedTodo);
    });

    expect(result.current.todos[0]?.is_completed).toBe(false);
  });

  it('should refresh todos when refresh is called', async () => {
    vi.mocked(todosApi.fetchTodos).mockResolvedValue({ todos: [], count: 0 });

    const { result } = renderHook(() => useTodos());

    await waitFor(() => {
      expect(result.current.isLoading).toBe(false);
    });

    vi.mocked(todosApi.fetchTodos).mockResolvedValue(mockListResponse);

    await act(async () => {
      await result.current.refresh();
    });

    expect(result.current.todos).toHaveLength(1);
  });
});
