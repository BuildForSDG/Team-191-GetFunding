import React, { useState } from 'react';
import {Link} from 'react-router-dom';

export default function RegisterLender() {
    
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");


  const handleSubmit = (e) => {
    e.preventDefault();
  }
  
  return (
    <div className="row">
      <div className="card card-body mt-4 mb-4 col-md-4 offset-4 col-sm-12">
        <h2>Register as a Lender</h2>
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label>Email</label>
            <input
              className="form-control"
              type="email"
              name="email"
              onChange={e => setEmail(e.target.value)}
              value={email}
              placeholder = "joedoe@email.com"
              required
            />
          </div>
          <div className="form-group">
            <label>password</label>
            <input
              className="form-control"
              type="password"
              name="password"
              onChange={e => setPassword(e.target.value)}
              value={password}
              minLength="8"
              required
              placeholder="********"
            />
          </div>
          <div className="form-group">
            <label>Confirm password</label>
            <input
              className="form-control"
              type="password"
              name="confirm_password"
              onChange={e => setConfirmPassword(e.target.value)}
              value={confirmPassword}
              minLength="8"
              required
              placeholder="********"
            />
          </div>
          <div className="form-group">
            <button type="submit" className="btn btn-primary">
              Register
            </button>
          </div>
          <p>
            Already have an account? <Link to="/login">Login</Link>
          </p>
        </form>
      </div>

    </div>
  )
}
