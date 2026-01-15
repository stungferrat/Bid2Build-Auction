<div align="center">

# 🏗️ Bid2Build

A real-time auction management platform built for IEEE events where teams compete for hardware components using limited credits.

[![Made with Streamlit](https://img.shields.io/badge/Made%20with-Streamlit-FF4B4B?style=for-the-badge&logo=streamlit)](https://streamlit.io)
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)

---

</div>

## 🎯 What is Bid2Build?

Bid2Build is a web platform that manages live technical auctions during team-based hackathons and engineering events. Instead of giving everyone the same components, teams strategically bid for hardware using limited credits.

The platform tracks everything in real-time:
- 💰 Team credits and spending
- 🔧 Component ownership
- 📊 Live auction history
- ✅ Instant error correction

Built for an IEEE Signal Processing Society event and tested under real competition conditions.

---

## 🌟 Why This Exists

As an IEEE organizer, I faced a problem: **How do you track dozens of components across multiple teams without mistakes?**

Manual spreadsheets fail. Paper logs get messy. Teams get confused about what they own.

**Bid2Build solved this.** One centralized system. Zero confusion. Real-time updates.

---

## ⚡ How It Works During an Event

### **Pre-Event Setup**
1. Admin configures teams and starting credits
2. Components and minimum bids are loaded
3. Team login credentials are distributed

### **Live Auction**
```
┌─────────────────────────────────────────┐
│  Physical Auction (Organizer calls bids)│
│               ↓                         │
│  Admin enters winning team + amount     │
│               ↓                         │
│  Platform updates in real-time          │
│               ↓                         │
│  Teams see updated credits & components │
└─────────────────────────────────────────┘
```

### **Team Experience**
- Log in to personal dashboard
- See remaining credits update live
- View all won components

### **Admin Control**
- Record auction results instantly
- Fix mistakes without stopping the event
- Export complete records to Excel
- Monitor all teams simultaneously

---

## 👥 Platform Roles

<table>
<tr>
<td width="50%">

### 🔑 **Admin**
- Controls all auction entries
- Assigns components to teams
- Manages credit allocation
- Corrects errors in real-time
- Exports final results

</td>
<td width="50%">

### 👨‍💻 **Teams**
- Secure login per team
- View personal dashboard only
- Track remaining credits
- See owned components
- Cannot access other team data

</td>
</tr>
</table>

---

## 🛠️ Tech Stack
```
┌─────────────────────────────────────────────┐
│                 Frontend                    │
│  Streamlit (Python-based web interface)     │
├─────────────────────────────────────────────┤
│                 Backend                     │
│  Python (Core logic & application flow)     │
├─────────────────────────────────────────────┤
│              Data Storage                   │
│  JSON (Lightweight, file-based)             │
├─────────────────────────────────────────────┤
│             Authentication                  │
│  Session-based, role-separated access       │
├─────────────────────────────────────────────┤
│              Deployment                     │
│  Streamlit Cloud (Free hosting)             │
├─────────────────────────────────────────────┤
│               Export                        │
│  Excel/XLSX (Audit trail & records)         │
└─────────────────────────────────────────────┘
```

**Why these choices?**
- **Streamlit**: Rapid deployment, no frontend coding needed.
- **JSON**: Simple, version-controllable, no database setup.
- **Python**: Easy to understand.
- **Streamlit Cloud**: Free, reliable, zero DevOps.

---

## 📸 Screenshots

<div align="center">

### Admin Dashboard
*Manage teams, credits, and auction results*

![Admin Dashboard Placeholder](https://via.placeholder.com/800x400/4A90E2/FFFFFF?text=Admin+Dashboard)

### Team Dashboard
*Track your credits and components*

![Team Dashboard Placeholder](https://via.placeholder.com/800x400/7ED321/FFFFFF?text=Team+Dashboard)

</div>

---

## 🚀 Quick Start

### Prerequisites
```bash
Python 3.8+
pip
```

### Installation
```bash
# Clone the repository
git clone https://github.com/yourusername/bid2build.git
cd bid2build

# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run app.py
```

### Configuration

Edit `config.json` to set up your event:
```json
{
  "teams": [
    {"name": "Team Alpha", "credits": 1000},
    {"name": "Team Beta", "credits": 1000}
  ],
  "components": [
    {"name": "Raspberry Pi 4", "min_bid": 300},
    {"name": "Arduino Uno", "min_bid": 150}
  ]
}
```

---

## ⚠️ Known Limitations

This platform was built for **real-world simplicity**, not feature completeness:

| Limitation | Why It Exists |
|------------|---------------|
| **Physical bidding only** | Keeps the event social and competitive |
| **JSON storage instead of database** | Easier to debug during live events |
| **Designed for small/medium events** | Prioritizes reliability over scale |
| **No automated bidding** | Organizers control the pace |

These aren't bugs—they're intentional design choices for event reliability.

---

## 📈 Real-World Impact

**Used at IEEE SPS Technical Event**
- ✅ Managed 8 teams across 3-hour auction
- ✅ Zero tracking errors
- ✅ Instant credit updates
- ✅ Complete audit trail exported to Excel
- ✅ Reduced organizer stress significantly

> *"This platform turned chaos into clarity. We could focus on running the event instead of tracking spreadsheets."*  
> — Event Organizer, IEEE SPS

---

## 🤝 Contributing

Contributions are welcome! Here's how:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📋 Roadmap

- [ ] Add multi-event support
- [ ] Implement SQLite backend option
- [ ] Create mobile-responsive design
- [ ] Add real-time notifications
- [ ] Support component trading between teams
- [ ] Generate automatic event reports

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

---

## 🙏 Acknowledgments

- Built for **IEEE Student Branch** events
- Inspired by real problems in technical event organization
- Tested and refined during live competitions
- Special thanks to all organizers who provided feedback

---

<div align="center">

### Built with ❤️ for the maker community

**[⭐ Star this repo](/)** if you find it useful!

Made by [Your Name](https://github.com/yourusername) | [IEEE Member](https://ieee.org)

</div>
