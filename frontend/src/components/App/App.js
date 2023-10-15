import { Routes, Route } from 'react-router-dom';
import BestRoute from '../BestRoute/BestRoute';
import Chat from '../Chat/Chat';
import Main from '../Main/Main';
import './App.css';
import Mark from '../Mark/Mark';

function App() {
  return (
    <div className="app">
      <Routes>
        <Route path="/" element={<Main />} />
        <Route path="/chat" element={<Chat />} />
        <Route path="/best-route" element={<BestRoute />} />
        <Route path="/test" element={
          <div style={{ background: "black" }}>
            <Mark percentage="5" />
            <Mark percentage="40" />
            <Mark percentage="90" />
          </div>
        } />
      </Routes>
    </div>
  );
}

export default App;
