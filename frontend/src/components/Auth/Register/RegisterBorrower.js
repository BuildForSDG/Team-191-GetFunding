import React, { useState } from "react";
import {Link} from "react-router-dom";

export default function RegisterBorrower() {
    
  const [phone, setPhone] = useState("");
  const [pin, setPin] = useState("");
  const [confirmPin, setConfirmPin] = useState("");

  const handleSubmit = (e) => {
      e.preventDefault();
  }

    return (
        <div className="row">
            <div className="card card-body mt-4 mb-4 col-md-4 offset-4">
                <h2>Sign up as a Borrower</h2>
                <form onSubmit={handleSubmit}>
                <div className="form-group">
                    <label>Phone Number</label>
                    <input
                    className="form-control"
                    type="tel"
                    name="tel"
                    onChange={e => setPhone(e.target.value)}
                    value={phone}
                    placeholder = "+254722222222"
                    required
                    />
                </div>
                <div className="form-group">
                    <label>pin</label>
                    <input
                    className="form-control"
                    type="password"
                    name="pin"
                    onChange={e => setPin(e.target.value)}
                    value={pin}
                    minLength="4"
                    inputmode="numeric"
                    required
                    placeholder = "****"
                    />
                </div>
                <div className="form-group">
                    <label>Confirm pin</label>
                    <input
                    className="form-control"
                    type="password"
                    name="confirm pin"
                    onChange={e => setConfirmPin(e.target.value)}
                    value={confirmPin}
                    minLength="4"
                    inputmode="numeric"
                    required
                    placeholder = "****"
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
