import { useMemo, useState } from 'react'
import './index.css'

const USERS_KEY = 'todo_auth_users_v1'
const SESSION_KEY = 'todo_auth_session_v1'
const TODOS_KEY_PREFIX = 'todo_auth_todos_v1:'

function readJson(key, fallback) {
  try {
    const raw = localStorage.getItem(key)
    return raw ? JSON.parse(raw) : fallback
  } catch {
    return fallback
  }
}

function writeJson(key, value) {
  localStorage.setItem(key, JSON.stringify(value))
}

function hashPassword(input) {
  // Lightweight browser hash for demo auth; not for production-grade security.
  return btoa(unescape(encodeURIComponent(input))).split('').reverse().join('')
}

function App() {
  const [users, setUsers] = useState(() => readJson(USERS_KEY, []))
  const [session, setSession] = useState(() => readJson(SESSION_KEY, null))
  const [todos, setTodos] = useState(() => {
    if (!session?.email) return []
    return readJson(`${TODOS_KEY_PREFIX}${session.email}`, [])
  })

  const [loginEmail, setLoginEmail] = useState('')
  const [loginPassword, setLoginPassword] = useState('')
  const [registerName, setRegisterName] = useState('')
  const [registerEmail, setRegisterEmail] = useState('')
  const [registerPassword, setRegisterPassword] = useState('')
  const [newTodo, setNewTodo] = useState('')
  const [error, setError] = useState('')

  const activeUser = useMemo(() => {
    if (!session?.email) return null
    return users.find((u) => u.email === session.email) || null
  }, [session, users])

  function persistUsers(nextUsers) {
    setUsers(nextUsers)
    writeJson(USERS_KEY, nextUsers)
  }

  function persistTodos(nextTodos, email = session?.email) {
    setTodos(nextTodos)
    if (email) writeJson(`${TODOS_KEY_PREFIX}${email}`, nextTodos)
  }

  function setActiveSession(nextSession) {
    setSession(nextSession)
    writeJson(SESSION_KEY, nextSession)
    if (!nextSession?.email) {
      setTodos([])
      return
    }
    setTodos(readJson(`${TODOS_KEY_PREFIX}${nextSession.email}`, []))
  }

  function register(e) {
    e.preventDefault()
    setError('')

    if (!registerName.trim() || !registerEmail.trim() || !registerPassword.trim()) {
      setError('Please complete all registration fields.')
      return
    }

    const email = registerEmail.trim().toLowerCase()
    if (users.some((u) => u.email === email)) {
      setError('This email is already registered.')
      return
    }

    const nextUsers = [
      ...users,
      {
        name: registerName.trim(),
        email,
        passwordHash: hashPassword(registerPassword),
      },
    ]

    persistUsers(nextUsers)
    setActiveSession({ email })
    persistTodos([], email)

    setRegisterName('')
    setRegisterEmail('')
    setRegisterPassword('')
  }

  function login(e) {
    e.preventDefault()
    setError('')

    const email = loginEmail.trim().toLowerCase()
    const user = users.find((u) => u.email === email)
    if (!user || user.passwordHash !== hashPassword(loginPassword)) {
      setError('Invalid email or password.')
      return
    }

    setActiveSession({ email })
    setLoginEmail('')
    setLoginPassword('')
  }

  function logout() {
    setActiveSession(null)
    setError('')
  }

  function addTodo(e) {
    e.preventDefault()
    const text = newTodo.trim()
    if (!text) return

    const nextTodos = [
      {
        id: crypto.randomUUID(),
        text,
        done: false,
        createdAt: Date.now(),
      },
      ...todos,
    ]
    persistTodos(nextTodos)
    setNewTodo('')
  }

  function toggleTodo(id) {
    persistTodos(todos.map((todo) => (todo.id === id ? { ...todo, done: !todo.done } : todo)))
  }

  function deleteTodo(id) {
    persistTodos(todos.filter((todo) => todo.id !== id))
  }

  const doneCount = todos.filter((t) => t.done).length

  return (
    <div className="page">
      <div className="panel">
        <h1>Todo Cloud Lite</h1>
        <p className="subtitle">Login/Register + Todo list, ready to deploy on Vercel.</p>

        {error ? <p className="error">{error}</p> : null}

        {!session ? (
          <div className="auth-grid">
            <form className="card" onSubmit={login}>
              <h2>Login</h2>
              <input
                placeholder="Email"
                type="email"
                value={loginEmail}
                onChange={(e) => setLoginEmail(e.target.value)}
                required
              />
              <input
                placeholder="Password"
                type="password"
                value={loginPassword}
                onChange={(e) => setLoginPassword(e.target.value)}
                required
              />
              <button type="submit">Login</button>
            </form>

            <form className="card" onSubmit={register}>
              <h2>Register</h2>
              <input
                placeholder="Name"
                value={registerName}
                onChange={(e) => setRegisterName(e.target.value)}
                required
              />
              <input
                placeholder="Email"
                type="email"
                value={registerEmail}
                onChange={(e) => setRegisterEmail(e.target.value)}
                required
              />
              <input
                placeholder="Password"
                type="password"
                value={registerPassword}
                onChange={(e) => setRegisterPassword(e.target.value)}
                required
              />
              <button type="submit">Create account</button>
            </form>
          </div>
        ) : (
          <div className="card">
            <div className="row between">
              <div>
                <h2>Welcome, {activeUser?.name || session.email}</h2>
                <p className="hint">
                  {doneCount}/{todos.length} completed
                </p>
              </div>
              <button className="ghost" onClick={logout}>
                Logout
              </button>
            </div>

            <form className="row" onSubmit={addTodo}>
              <input
                placeholder="Add a new todo"
                value={newTodo}
                onChange={(e) => setNewTodo(e.target.value)}
              />
              <button type="submit">Add</button>
            </form>

            <ul className="todo-list">
              {todos.length === 0 ? <li className="hint">No todos yet.</li> : null}
              {todos.map((todo) => (
                <li key={todo.id} className="todo-item">
                  <label>
                    <input type="checkbox" checked={todo.done} onChange={() => toggleTodo(todo.id)} />
                    <span className={todo.done ? 'done' : ''}>{todo.text}</span>
                  </label>
                  <button className="danger" onClick={() => deleteTodo(todo.id)}>
                    Delete
                  </button>
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>
    </div>
  )
}

export default App
