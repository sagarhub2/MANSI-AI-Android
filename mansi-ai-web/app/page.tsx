"use client";
import { useState } from "react";

type Message = { role: "user" | "assistant"; content: string };

export default function Home() {
  const [prompt, setPrompt] = useState("");
  const [persona, setPersona] = useState("Mansi");
  const [roast, setRoast] = useState(false);
  const [messages, setMessages] = useState<Message[]>([
    { role: "assistant", content: "Hii Sagarrr! 💗 Main MANSI hoon. Aaj kya create ya explore karein?" }
  ]);
  const [busy, setBusy] = useState(false);

  async function sendMessage() {
    const value = prompt.trim();
    if (!value || busy) return;
    setMessages((m) => [...m, { role: "user", content: value }]);
    setPrompt("");
    setBusy(true);
    try {
      const response = await fetch("/api/chat", {
        method: "POST", headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: value, persona, roast })
      });
      const data = await response.json();
      setMessages((m) => [...m, { role: "assistant", content: data.reply ?? data.error ?? "AI response missing." }]);
    } catch {
      setMessages((m) => [...m, { role: "assistant", content: "Backend abhi connect nahi hai. Deployment settings check karo." }]);
    } finally { setBusy(false); }
  }

  return <main className="shell">
    <nav className="nav"><a className="brand" href="#"><span className="brandMark">M</span> MANSI<span className="muted">.AI</span></a><div className="navLinks"><a href="#features">Features</a><a href="#chat">Chat</a><a href="#about">About</a></div><a className="navCta" href="#chat">Open Mansi ↗</a></nav>
    <section className="hero">
      <div className="eyebrow"><span className="pulse" /> YOUR PERSONAL AI COMPANION</div>
      <h1>More than AI.<br/><span>Your world, understood.</span></h1>
      <p className="heroText">Meet MANSI — a thoughtful, creative AI companion for conversations, ideas, coding and everything in between.</p>
      <div className="heroActions"><a className="primary" href="#chat">Start chatting <span>↗</span></a><a className="secondary" href="#features">Explore features</a></div>
      <div className="orbWrap"><div className="orb"><div className="orbCore">M</div></div><div className="orbit orbitOne"/><div className="orbit orbitTwo"/><span className="floatTag tagA">✦ Always here</span><span className="floatTag tagB">♡ Your space</span></div>
      <div className="heroFoot"><span>CREATIVE THINKING</span><span>PERSONAL CONVERSATIONS</span><span>BUILT TO INSPIRE</span></div>
    </section>
    <section id="features" className="features">
      <div className="sectionHead"><div><div className="eyebrow">WHAT YOU CAN DO</div><h2>One companion.<br/><span>Many possibilities.</span></h2></div><p>From a quick question to a big idea, MANSI helps you move from thinking to doing.</p></div>
      <div className="featureGrid">
        <article className="featureCard"><b>✧</b><h3>Smart conversations</h3><p>Natural chat for questions, planning, learning and everyday ideas.</p></article>
        <article className="featureCard"><b>⌘</b><h3>Code & create</h3><p>Explore code, debug problems and shape new digital projects.</p></article>
        <article className="featureCard"><b>♡</b><h3>Your style</h3><p>Choose a persona and tune the conversation to your mood.</p></article>
      </div>
    </section>
    <section id="chat" className="chatSection">
      <div className="sectionHead"><div><div className="eyebrow">TRY THE EXPERIENCE</div><h2>Say hello to <span>MANSI.</span></h2></div><p>Chat with MANSI, choose a persona or turn on friendly Roast Mode.</p></div>
      <div className="chatPanel">
        <div className="chatTop"><div className="status"><span className="pulse"/> MANSI ACTIVE</div><span className="tiny">PRIVATE SPACE · WEB</span></div>
        <div className="chatTools"><label>PERSONA <select value={persona} onChange={e=>setPersona(e.target.value)}><option>Mansi</option><option>Creative</option><option>Study Buddy</option><option>Developer</option></select></label><label className="switchLabel"><input type="checkbox" checked={roast} onChange={e=>setRoast(e.target.checked)}/> Roast mode</label></div>
        <div className="messages">{messages.map((m,i)=><div key={i} className={`message ${m.role}`}><span>{m.role==="assistant"?"M":"YOU"}</span><p>{m.content}</p></div>)}{busy&&<div className="typing">MANSI is thinking<span>•••</span></div>}</div>
        <div className="composer"><input value={prompt} onChange={e=>setPrompt(e.target.value)} onKeyDown={e=>e.key==="Enter"&&sendMessage()} placeholder="Message MANSI..." /><button onClick={sendMessage} disabled={busy}>Send ↗</button></div>
        <p className="disclaimer">AI replies require Gemini server configuration.</p>
      </div>
    </section>
    <footer id="about"><a className="brand" href="#"><span className="brandMark">M</span> MANSI<span className="muted">.AI</span></a><span>Made for ideas that matter. © 2026 MANSI AI</span></footer>
  </main>;
}