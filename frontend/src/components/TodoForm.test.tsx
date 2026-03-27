import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { TodoForm } from './TodoForm';

beforeEach(() => {
  vi.resetAllMocks();
});

describe('TodoForm', () => {
  it('should render title input and submit button', () => {
    render(<TodoForm onSubmit={vi.fn()} />);

    expect(screen.getByLabelText(/todo title/i)).toBeInTheDocument();
  });

  it('should expand to show description and buttons on focus', async () => {
    const user = userEvent.setup();
    render(<TodoForm onSubmit={vi.fn()} />);

    const titleInput = screen.getByLabelText(/todo title/i);
    await user.click(titleInput);

    expect(screen.getByLabelText(/todo description/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /add todo/i })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /cancel/i })).toBeInTheDocument();
  });

  it('should call onSubmit with title and description when form is submitted', async () => {
    const user = userEvent.setup();
    const onSubmit = vi.fn().mockResolvedValue(undefined);
    render(<TodoForm onSubmit={onSubmit} />);

    const titleInput = screen.getByLabelText(/todo title/i);
    await user.click(titleInput);
    await user.type(titleInput, 'Buy groceries');

    const descInput = screen.getByLabelText(/todo description/i);
    await user.type(descInput, 'Milk and eggs');

    await user.click(screen.getByRole('button', { name: /add todo/i }));

    expect(onSubmit).toHaveBeenCalledWith({
      title: 'Buy groceries',
      description: 'Milk and eggs',
    });
  });

  it('should clear inputs after successful submission', async () => {
    const user = userEvent.setup();
    const onSubmit = vi.fn().mockResolvedValue(undefined);
    render(<TodoForm onSubmit={onSubmit} />);

    const titleInput = screen.getByLabelText(/todo title/i);
    await user.click(titleInput);
    await user.type(titleInput, 'Test task');
    await user.click(screen.getByRole('button', { name: /add todo/i }));

    expect(titleInput).toHaveValue('');
  });

  it('should show error when submitting empty title', async () => {
    const user = userEvent.setup();
    const onSubmit = vi.fn();
    render(<TodoForm onSubmit={onSubmit} />);

    const titleInput = screen.getByLabelText(/todo title/i);
    await user.click(titleInput);

    // Type and clear to trigger expanded state while keeping title empty
    await user.type(titleInput, ' ');
    await user.clear(titleInput);

    // Submit button should be disabled when title is empty
    const submitButton = screen.getByRole('button', { name: /add todo/i });
    expect(submitButton).toBeDisabled();
    expect(onSubmit).not.toHaveBeenCalled();
  });

  it('should show error message when onSubmit rejects', async () => {
    const user = userEvent.setup();
    const onSubmit = vi.fn().mockRejectedValue(new Error('API error'));
    render(<TodoForm onSubmit={onSubmit} />);

    const titleInput = screen.getByLabelText(/todo title/i);
    await user.click(titleInput);
    await user.type(titleInput, 'Valid title');
    await user.click(screen.getByRole('button', { name: /add todo/i }));

    expect(await screen.findByText(/failed to create todo/i)).toBeInTheDocument();
  });

  it('should collapse form when cancel is clicked', async () => {
    const user = userEvent.setup();
    render(<TodoForm onSubmit={vi.fn()} />);

    const titleInput = screen.getByLabelText(/todo title/i);
    await user.click(titleInput);

    expect(screen.getByLabelText(/todo description/i)).toBeInTheDocument();

    await user.click(screen.getByRole('button', { name: /cancel/i }));

    expect(screen.queryByLabelText(/todo description/i)).not.toBeInTheDocument();
  });

  it('should submit with null description when description is empty', async () => {
    const user = userEvent.setup();
    const onSubmit = vi.fn().mockResolvedValue(undefined);
    render(<TodoForm onSubmit={onSubmit} />);

    const titleInput = screen.getByLabelText(/todo title/i);
    await user.click(titleInput);
    await user.type(titleInput, 'No desc task');
    await user.click(screen.getByRole('button', { name: /add todo/i }));

    expect(onSubmit).toHaveBeenCalledWith({
      title: 'No desc task',
      description: null,
    });
  });
});
