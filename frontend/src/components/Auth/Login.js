import React, { useState } from "react";
import {Link} from "react-router-dom";

export default function Login() {
    const [phone, setPhone] = useState("");
    const [pin, setPin] = useState("");

    const handleSubmit = (e) => {
        e.preventDefault();
    }

    return (
        <div className="col-md-4 offset-4 col-sm-12">
            <div className="card card-body mt-4 mb-4">
                <h2>Login</h2>
                <form onSubmit={handleSubmit}>
                <div className="form-group">
                    <label>Phone no.</label>
                    <input
                    className="form-control"
                    type="tel"
                    name="tel"
                    onChange={e => setPhone(e.target.value)}
                    value={phone}
                    inputmode="numeric"
                    required
                    minLength="8"
                    placeholder="+254722222222"
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
                    placeholder="****"
                    />
                </div>
                <div className="form-group">
                    <button type="submit" className="btn btn-primary">
                        Login
                    </button>
                </div>
                <p>
                    Create an account <Link to="/register">register</Link>
                </p>
                </form>
            </div>
        </div>
    )
}
