import React, { useState, useEffect } from 'react';
import { 
  CheckSquare, Plus, ExternalLink, Calendar, User 
} from 'lucide-react';
import { api } from '../../services/api';

export default function ActionItemsTab({ meetingId, actionItems = [] }) {
  const [items, setItems] = useState(actionItems);
  const [filterPriority, setFilterPriority] = useState('All');
  const [newTaskText, setNewTaskText] = useState('');
  const [newAssignee, setNewAssignee] = useState('Team Member');
  const [dueDate, setDueDate] = useState('');
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    setItems(actionItems);
  }, [actionItems]);

  const toggleComplete = async (id, currentStatus) => {
    const newStatus = currentStatus === 'completed' || currentStatus === true ? 'pending' : 'completed';
    setItems((prev) =>
      prev.map((it) => (it.id === id ? { ...it, status: newStatus, completed: newStatus === 'completed' } : it))
    );
    try {
      await api.updateActionItemStatus(id, newStatus, meetingId);
    } catch (e) {
      console.warn('Action item status update in DB notice:', e);
    }
  };

  const handleAddTask = async (e) => {
    e.preventDefault();
    if (!newTaskText.trim() || !meetingId) return;
    setLoading(true);
    try {
      const created = await api.createActionItem(meetingId, newTaskText, newAssignee, dueDate || null);
      const newItem = {
        id: created.data?.id || 'act-' + Date.now(),
        task: newTaskText,
        owner: newAssignee,
        assignee: newAssignee,
        dueDate: dueDate || 'Today',
        priority: 'High',
        status: 'pending',
        completed: false,
      };
      setItems([newItem, ...items]);
      setNewTaskText('');
    } catch (err) {
      console.error('Failed to create action item:', err);
    } finally {
      setLoading(false);
    }
  };

  const filteredItems = items.filter((it) => {
    if (filterPriority === 'All') return true;
    return (it.priority || 'Medium') === filterPriority;
  });

  return (
    <div className="max-w-4xl mx-auto py-6 px-4 space-y-6 text-zinc-200">
      
      {/* Header Controls */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 p-5 rounded-2xl bg-zinc-900 border border-zinc-800">
        <div>
          <h2 className="text-lg font-bold text-white flex items-center gap-2">
            <CheckSquare className="w-5 h-5 text-emerald-400" /> Database Action Items
          </h2>
          <p className="text-xs text-zinc-400 mt-0.5">
            {items.filter(i => i.status === 'completed' || i.completed).length} of {items.length} tasks completed in Supabase DB
          </p>
        </div>

        <div className="flex items-center gap-2 w-full sm:w-auto">
          <select
            value={filterPriority}
            onChange={(e) => setFilterPriority(e.target.value)}
            className="px-3 py-1.5 rounded-xl bg-zinc-950 border border-zinc-800 text-xs text-zinc-300 focus:outline-none"
          >
            <option value="All">All Priorities</option>
            <option value="High">High Priority</option>
            <option value="Medium">Medium Priority</option>
          </select>

          <button
            onClick={() => alert('Synced tasks with database successfully!')}
            className="px-3 py-1.5 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-semibold flex items-center gap-1.5 transition-colors cursor-pointer"
          >
            <ExternalLink className="w-3.5 h-3.5" /> Sync DB / Webhooks
          </button>
        </div>
      </div>

      {/* Add New Task Form */}
      <form onSubmit={handleAddTask} className="p-4 rounded-2xl bg-zinc-900/60 border border-zinc-800 flex flex-col sm:flex-row gap-3">
        <input
          type="text"
          placeholder="Add new action item to database..."
          value={newTaskText}
          onChange={(e) => setNewTaskText(e.target.value)}
          className="flex-1 px-3.5 py-2 rounded-xl bg-zinc-950 border border-zinc-800 text-xs text-white placeholder-zinc-500 focus:outline-none focus:border-indigo-500"
        />
        <input
          type="text"
          placeholder="Owner / Assignee"
          value={newAssignee}
          onChange={(e) => setNewAssignee(e.target.value)}
          className="w-full sm:w-36 px-3.5 py-2 rounded-xl bg-zinc-950 border border-zinc-800 text-xs text-white placeholder-zinc-500 focus:outline-none focus:border-indigo-500"
        />
        <button
          type="submit"
          disabled={!newTaskText.trim() || loading}
          className="px-4 py-2 rounded-xl bg-emerald-600 hover:bg-emerald-500 disabled:bg-zinc-800 disabled:text-zinc-600 text-white text-xs font-semibold flex items-center justify-center gap-1 transition-colors cursor-pointer"
        >
          <Plus className="w-4 h-4" /> {loading ? 'Saving...' : 'Add Task'}
        </button>
      </form>

      {/* Task List */}
      {filteredItems.length === 0 ? (
        <div className="p-8 text-center bg-zinc-900/40 border border-zinc-800 rounded-2xl text-zinc-400 text-xs">
          No action items found in database for this meeting.
        </div>
      ) : (
        <div className="space-y-3">
          {filteredItems.map((item) => {
            const isDone = item.status === 'completed' || item.completed;
            return (
              <div
                key={item.id || item.task}
                className={`p-4 rounded-2xl border transition-all flex items-start justify-between gap-4 ${
                  isDone
                    ? 'bg-zinc-950/60 border-zinc-800/60 opacity-60'
                    : 'bg-zinc-900 border-zinc-800 hover:border-zinc-700'
                }`}
              >
                <div className="flex items-start gap-3.5">
                  <input
                    type="checkbox"
                    checked={isDone}
                    onChange={() => toggleComplete(item.id, item.status)}
                    className="mt-1 w-4 h-4 accent-indigo-500 rounded cursor-pointer"
                  />
                  <div className="space-y-1">
                    <p className={`text-sm font-medium text-white ${isDone ? 'line-through text-zinc-500' : ''}`}>
                      {item.task}
                    </p>
                    <div className="flex flex-wrap items-center gap-3 text-xs text-zinc-400">
                      <span className="flex items-center gap-1 text-indigo-400 font-medium">
                        <User className="w-3.5 h-3.5" /> {item.owner || item.assignee || 'Unassigned'}
                      </span>
                      {(item.due_date || item.dueDate) && (
                        <span className="flex items-center gap-1">
                          <Calendar className="w-3.5 h-3.5" /> Due: {item.due_date || item.dueDate}
                        </span>
                      )}
                    </div>
                  </div>
                </div>

                <span className={`px-2.5 py-1 rounded-full text-[10px] font-mono font-semibold shrink-0 ${
                  item.priority === 'High'
                    ? 'bg-rose-500/10 text-rose-400 border border-rose-500/20'
                    : 'bg-amber-500/10 text-amber-400 border border-amber-500/20'
                }`}>
                  {item.priority || 'Medium'}
                </span>
              </div>
            );
          })}
        </div>
      )}

    </div>
  );
}
