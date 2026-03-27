import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { TodoItem } from './TodoItem';
import type { Todo } from '../types/todo';

const baseTodo: Todo = {
  id: 1,
  title: 'Buy groceries',
  description: 'Milk, eggs, bread',
  is_completed: false,
  created_at: '2025-01-15T10:30:00Z',
  updated_at: '2025-01-15T10:30:00Z',
};

const defaultProps = () => ({
  todo: { ...baseTodo },
  onToggleComplete: vi.fn().mockResolvedValue(undefined),
  onDelete: vi.fn().mockResolvedValue(undefined),
  onEdit: vi.fn().mockResolvedValue(undefined),
});

beforeEach(() => {
  vi.resetAllMocks();
});

describe('TodoItem', () => {
  it('should render title, description, and formatted date', () => {
    render(<TodoItem {...defaultProps()} />);

    expect(screen.getByText('Buy groceries')).toBeInTheDocument();
    expect(screen.getByText('Milk, eggs, bread')).toBeInTheDocument();
    expect(screen.getByText('Jan 15')).toBeInTheDocument();
  });

  it('should apply line-through style when todo is completed', () => {
    const props = defaultProps();
    props.todo.is_completed = true;

    render(<TodoItem {...props} />);

    const title = screen.getByText('Buy groceries');
    expect(title).toHaveClass('line-through');
  });

  it('should not apply line-through style when todo is incomplete', () => {
    render(<TodoItem {...defaultProps()} />);

    const title = screen.getByText('Buy groceries');
    expect(title).not.toHaveClass('line-through');
  });

  it('should call onToggleComplete when checkbox is clicked', async () => {
    const user = userEvent.setup();
    const props = defaultProps();
    render(<TodoItem {...props} />);

    const checkbox = screen.getByRole('button', {
      name: /mark "Buy groceries" as complete/i,
    });
    await user.click(checkbox);

    expect(props.onToggleComplete).toHaveBeenCalledWith(props.todo);
  });

  it('should call onDelete when delete button is clicked', async () => {
    const user = userEvent.setup();
    const props = defaultProps();
    render(<TodoItem {...props} />);

    const deleteBtn = screen.getByRole('button', { name: /delete todo/i });
    await user.click(deleteBtn);

    expect(props.onDelete).toHaveBeenCalledWith(1);
  });

  it('should enter edit mode when edit button is clicked', async () => {
    const user = userEvent.setup();
    render(<TodoItem {...defaultProps()} />);

    await user.click(screen.getByRole('button', { name: /edit todo/i }));

    expect(screen.getByLabelText(/edit title/i)).toHaveValue('Buy groceries');
    expect(screen.getByLabelText(/edit description/i)).toHaveValue('Milk, eggs, bread');
  });

  it('should call onEdit with updated values when save is clicked', async () => {
    const user = userEvent.setup();
    const props = defaultProps();
    render(<TodoItem {...props} />);

    await user.click(screen.getByRole('button', { name: /edit todo/i }));

    const titleInput = screen.getByLabelText(/edit title/i);
    await user.clear(titleInput);
    await user.type(titleInput, 'Updated title');

    await user.click(screen.getByRole('button', { name: /save/i }));

    expect(props.onEdit).toHaveBeenCalledWith(1, {
      title: 'Updated title',
      description: 'Milk, eggs, bread',
    });
  });

  it('should revert changes when cancel is clicked in edit mode', async () => {
    const user = userEvent.setup();
    render(<TodoItem {...defaultProps()} />);

    await user.click(screen.getByRole('button', { name: /edit todo/i }));

    const titleInput = screen.getByLabelText(/edit title/i);
    await user.clear(titleInput);
    await user.type(titleInput, 'Changed');

    await user.click(screen.getByRole('button', { name: /cancel/i }));

    // Should be back to view mode with original title
    expect(screen.getByText('Buy groceries')).toBeInTheDocument();
    expect(screen.queryByLabelText(/edit title/i)).not.toBeInTheDocument();
  });

  it('should disable save button when edit title is empty', async () => {
    const user = userEvent.setup();
    render(<TodoItem {...defaultProps()} />);

    await user.click(screen.getByRole('button', { name: /edit todo/i }));

    const titleInput = screen.getByLabelText(/edit title/i);
    await user.clear(titleInput);

    expect(screen.getByRole('button', { name: /save/i })).toBeDisabled();
  });

  it('should not render description when todo has no description', () => {
    const props = defaultProps();
    props.todo.description = null;

    render(<TodoItem {...props} />);

    expect(screen.getByText('Buy groceries')).toBeInTheDocument();
    expect(screen.queryByText('Milk, eggs, bread')).not.toBeInTheDocument();
  });
});
