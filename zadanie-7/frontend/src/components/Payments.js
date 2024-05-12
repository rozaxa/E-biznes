import React, { useState } from 'react';

function Payments() {
    const [amount, setAmount] = useState('');

    const handleSubmit = (event) => {
        event.preventDefault();
        const amountNumber = parseFloat(amount);
        if (isNaN(amountNumber) || amountNumber <= 0) {
            console.error('Invalid amount value');
            return;
        }
        fetch('http://localhost:4000/payments', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ amount: amountNumber }),
        })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok ' + response.statusText);
                }
                return response.json();
            })
            .then(data => {
                console.log('Payment successful', data);
                alert(`Payment successful: ${amountNumber} has been paid.`);
                setAmount('');
            })
            .catch(error => {
                console.error('Error making payment', error);
            });
    };

    return (
        <div>
            <h2> Payments </h2>
            <form onSubmit={handleSubmit}>
                <label>
                    Amount:
                    <input
                        type="number"
                        value={amount}
                        onChange={e => setAmount(e.target.value)}
                        min="0.01"
                        step="0.01"
                    />
                </label>
                <button type="submit"> Pay </button>
            </form>
        </div>
    );
}

export default Payments;
