import React, { useState, useEffect } from 'react';

interface HistoryItem {
  period: string;
  number: number;
  bigSmall: 'Big' | 'Small';
  color: 'Green' | 'Red' | 'Violet';
}

export default function App() {
  const [balance, setBalance] = useState<number>(120000);
  const [selectedTime, setSelectedTime] = useState<string>('30s');
  const [timeLeft, setTimeLeft] = useState<number>(30);
  const [betAmount, setBetAmount] = useState<string>('120000');
  const [selectedBet, setSelectedBet] = useState<string>('Small');

  const [currentPage, setCurrentPage] = useState<
    'home' | 'game' | 'deposit' | 'login' | 'pending'
  >('home');

  const [phone, setPhone] = useState<string>('');
  const [password, setPassword] = useState<string>('');
  const [depositAmount, setDepositAmount] = useState<string>('50000');

  const [history, setHistory] = useState<HistoryItem[]>([
    {
      period: '20260518001051',
      number: 5,
      bigSmall: 'Big',
      color: 'Violet',
    },
    {
      period: '20260518001050',
      number: 5,
      bigSmall: 'Big',
      color: 'Violet',
    },
    {
      period: '20260518001049',
      number: 6,
      bigSmall: 'Big',
      color: 'Red',
    },
    {
      period: '20260518001048',
      number: 0,
      bigSmall: 'Small',
      color: 'Violet',
    },
    {
      period: '20260518001047',
      number: 0,
      bigSmall: 'Small',
      color: 'Violet',
    },
  ]);

  useEffect(() => {
    if (currentPage !== 'game') return;

    const timer = setInterval(() => {
      setTimeLeft((prev) => {
        if (prev <= 1) {
          generateRandomResult();
          return 30;
        }

        return prev - 1;
      });
    }, 1000);

    return () => clearInterval(timer);
  }, [currentPage]);

  const generateRandomResult = () => {
    const nextPeriod = String(
      Number(history[0]?.period || '20260518001000') + 1
    );

    const randNum = Math.floor(Math.random() * 10);

    const bigSmall = randNum >= 5 ? 'Big' : 'Small';

    const colors: ('Green' | 'Red' | 'Violet')[] = [
      'Green',
      'Red',
      'Violet',
    ];

    const randColor =
      colors[Math.floor(Math.random() * colors.length)];

    const newItem: HistoryItem = {
      period: nextPeriod,
      number: randNum,
      bigSmall,
      color: randColor,
    };

    setHistory([newItem, ...history]);
  };

  const handlePlaceBet = () => {
    const amount = Number(betAmount);

    if (isNaN(amount) || amount <= 0) {
      alert(
        'ကျေးဇူးပြု၍ တရားဝင်သော လောင်းကြေးပမာဏ ထည့်သွင်းပါ။'
      );
      return;
    }

    if (amount > balance) {
      alert('လက်ကျန်ငွေ မလုံလောက်ပါ။');
      return;
    }

    setBalance((prev) => prev - amount);

    alert(
      `လောင်းကြေးထည့်ပြီး - ${selectedBet} · Ks ${amount.toLocaleString()}`
    );
  };

  const renderHome = () => (
    <div className="max-w-md mx-auto bg-slate-100 min-h-screen text-slate-900 pb-10">
      <div className="bg-blue-600 text-white p-6 rounded-b-3xl shadow-md">
        <div className="flex justify-between items-center mb-4">
          <div>
            <p className="text-xs opacity-80">WELCOME BACK</p>
            <h1 className="text-2xl font-bold">Taro</h1>
          </div>

          <button
            onClick={() => setCurrentPage('login')}
            className="p-2 bg-blue-700 rounded-full"
          >
            🚪
          </button>
        </div>

        <p className="text-xs opacity-80">TOTAL BALANCE</p>

        <div className="text-3xl font-extrabold my-1">
          {balance.toLocaleString()} MMK
        </div>

        <div className="grid grid-cols-2 gap-4 mt-4">
          <button
            onClick={() => setCurrentPage('deposit')}
            className="bg-white text-blue-600 font-bold py-2 rounded-xl"
          >
            Deposit
          </button>

          <button
            className="bg-blue-500 text-white font-bold py-2 rounded-xl"
          >
            Withdraw
          </button>
        </div>
      </div>

      <div className="p-4">
        <h2 className="font-bold text-lg mb-3">
          🎮 Win Go Games
        </h2>

        <div className="grid grid-cols-2 gap-4">
          {['1Min', '3Min', '5Min', '10Min'].map((game) => (
            <div
              key={game}
              onClick={() => setCurrentPage('game')}
              className="bg-gradient-to-br from-pink-500 to-rose-600 text-white p-4 rounded-2xl shadow-sm cursor-pointer"
            >
              <h3 className="font-bold">Win Go {game}</h3>

              <p className="text-xs opacity-80">
                Tap to play
              </p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );

  const renderGame = () => (
    <div className="max-w-md mx-auto bg-slate-50 min-h-screen pb-10">
      <div className="bg-blue-600 text-white p-4 flex justify-between">
        <button onClick={() => setCurrentPage('home')}>
          ⬅ Back
        </button>

        <span className="font-bold">COLOR GAME</span>

        <div></div>
      </div>

      <div className="m-4 bg-white p-4 rounded-2xl shadow">
        <p className="text-xs text-slate-500">
          Wallet Balance
        </p>

        <div className="text-3xl font-black">
          Ks {balance.toLocaleString()}
        </div>
      </div>

      <div className="mx-4 grid grid-cols-4 gap-2">
        {['30s', '1Min', '3Min', '5Min'].map((time) => (
          <button
            key={time}
            onClick={() => setSelectedTime(time)}
            className={`py-2 rounded-lg font-bold ${
              selectedTime === time
                ? 'bg-blue-600 text-white'
                : 'bg-white'
            }`}
          >
            {time}
          </button>
        ))}
      </div>

      <div className="m-4 bg-white p-4 rounded-2xl shadow">
        <div className="flex justify-between">
          <div>
            <p className="text-xs text-slate-400">Time Left</p>

            <div className="text-3xl font-black text-red-500">
              00 : {timeLeft < 10 ? `0${timeLeft}` : timeLeft}
            </div>
          </div>

          <div>
            <p className="text-xs text-slate-400">
              Selected Bet
            </p>

            <div className="font-bold text-blue-600">
              {selectedBet}
            </div>
          </div>
        </div>
      </div>

      <div className="mx-4 bg-white p-4 rounded-2xl shadow">
        <div className="grid grid-cols-3 gap-3 mb-4">
          <button
            onClick={() => setSelectedBet('Green')}
            className="bg-green-500 text-white py-2 rounded-xl font-bold"
          >
            Green
          </button>

          <button
            onClick={() => setSelectedBet('Violet')}
            className="bg-purple-500 text-white py-2 rounded-xl font-bold"
          >
            Violet
          </button>

          <button
            onClick={() => setSelectedBet('Red')}
            className="bg-red-500 text-white py-2 rounded-xl font-bold"
          >
            Red
          </button>
        </div>

        <div className="grid grid-cols-5 gap-2 mb-4">
          {[0, 1, 2, 3, 4, 5, 6, 7, 8, 9].map((num) => (
            <button
              key={num}
              onClick={() =>
                setSelectedBet(String(num))
              }
              className="bg-blue-500 text-white h-12 rounded-full font-bold"
            >
              {num}
            </button>
          ))}
        </div>

        <div className="grid grid-cols-2 gap-3 mb-4">
          <button
            onClick={() => setSelectedBet('Big')}
            className="bg-orange-500 text-white py-3 rounded-xl font-bold"
          >
            Big
          </button>

          <button
            onClick={() => setSelectedBet('Small')}
            className="bg-cyan-500 text-white py-3 rounded-xl font-bold"
          >
            Small
          </button>
        </div>

        <input
          type="number"
          value={betAmount}
          onChange={(e) =>
            setBetAmount(e.target.value)
          }
          className="w-full border rounded-xl p-3 mb-4"
        />

        <button
          onClick={handlePlaceBet}
          className="w-full bg-blue-600 text-white font-bold py-3 rounded-xl"
        >
          Place Bet
        </button>
      </div>

      <div className="m-4 bg-white rounded-2xl shadow overflow-hidden">
        <table className="w-full text-sm">
          <thead className="bg-slate-100">
            <tr>
              <th className="p-2">Period</th>
              <th className="p-2">Number</th>
              <th className="p-2">Type</th>
              <th className="p-2">Color</th>
            </tr>
          </thead>

          <tbody>
            {history.map((item, idx) => (
              <tr key={idx}>
                <td className="p-2">{item.period}</td>

                <td className="p-2">
                  {item.number}
                </td>

                <td className="p-2">
                  {item.bigSmall}
                </td>

                <td className="p-2">
                  {item.color}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );

  const renderDeposit = () => (
    <div className="max-w-md mx-auto min-h-screen flex flex-col justify-center items-center bg-slate-900 text-white p-6">
      <h2 className="text-2xl font-bold mb-4">
        Deposit
      </h2>

      <input
        type="number"
        value={depositAmount}
        onChange={(e) =>
          setDepositAmount(e.target.value)
        }
        className="w-full p-3 rounded-xl text-black mb-4"
      />

      <button
        onClick={() => {
          alert(
            `Telegram Deposit Request ပို့ပြီးပါပြီ - ${depositAmount} MMK`
          );

          setCurrentPage('pending');
        }}
        className="w-full bg-blue-600 py-3 rounded-xl font-bold"
      >
        Send Request
      </button>
    </div>
  );

  const renderPending = () => (
    <div className="max-w-md mx-auto min-h-screen flex flex-col justify-center items-center">
      <h2 className="text-3xl font-bold mb-4">
        Waiting Approval...
      </h2>

      <button
        onClick={() => {
          setBalance(
            (prev) =>
              prev + Number(depositAmount || 0)
          );

          setCurrentPage('home');
        }}
        className="bg-blue-600 text-white px-6 py-3 rounded-xl"
      >
        Simulate Approve
      </button>
    </div>
  );

  const renderLogin = () => (
    <div className="max-w-md mx-auto min-h-screen bg-slate-100 p-6">
      <h1 className="text-3xl font-bold mb-6 text-center">
        Login
      </h1>

      <div className="bg-white p-5 rounded-2xl shadow">
        <input
          type="tel"
          placeholder="Phone Number"
          value={phone}
          onChange={(e) =>
            setPhone(e.target.value)
          }
          className="w-full border p-3 rounded-xl mb-4"
        />

        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) =>
            setPassword(e.target.value)
          }
          className="w-full border p-3 rounded-xl mb-4"
        />

        <button
          onClick={() => setCurrentPage('home')}
          className="w-full bg-blue-600 text-white py-3 rounded-xl font-bold"
        >
          Login
        </button>
      </div>
    </div>
  );

  return (
    <>
      {currentPage === 'home' && renderHome()}
      {currentPage === 'game' && renderGame()}
      {currentPage === 'deposit' && renderDeposit()}
      {currentPage === 'pending' && renderPending()}
      {currentPage === 'login' && renderLogin()}
    </>
  );
          }
