# 🎯 Quick Reference: Professional Profile RAG System

## 🚀 Quick Start Commands

```bash
# Navigate to project
cd /Users/DELL/ragfood

# Query your professional profile (CLI mode)
python3 vivian_profile_query.py "What are my salary expectations?"

# Interactive mode (continuous Q&A)
python3 vivian_profile_query.py

# Check database status
python3 check_upstash_database.py

# Re-upload profile (if you make changes)
python3 upload_vivian_profile_to_upstash.py
```

---

## 💬 Sample Questions (Copy-Paste Ready)

### **Compensation & Availability**
```
What are my salary expectations for contract roles?
What are my salary expectations for permanent roles?
Am I available for full-time work?
What's my work authorization status?
Am I willing to relocate?
Can I travel for work?
```

### **Technical Skills**
```
What are my Excel skills and achievements?
Do I have Power BI certification?
Tell me about my Python proficiency
What's my SQL experience?
What AI/ML tools do I know?
What's my strongest technical skill?
```

### **Projects (STAR Format)**
```
Tell me about a data quality project using STAR format
Describe my Excel dashboard project
What's the ragfood project?
How much time did I save through automation?
What accuracy improvements did I achieve?
```

### **Soft Skills**
```
How quickly can I learn new technologies?
Give me an example of effective teamwork
How do I handle multiple responsibilities?
What are my communication skills?
What's my time management track record?
```

### **Career & Goals**
```
What are my career goals?
Why do I want to work in data analysis?
What companies am I targeting?
What are my strengths for a data analyst role?
```

---

## 📊 Key Numbers to Remember

| Metric | Value | Source |
|--------|-------|--------|
| **Contract Rate** | $500-600/day | vivian-002 |
| **Permanent Salary** | $55k-70k/year | vivian-002 |
| **Excel Level** | 5 (Advanced-Expert) | vivian-006 |
| **Power BI** | Microsoft Certified | vivian-007 |
| **Time Reduction** | 70% (15hrs → 4hrs/week) | vivian-012 |
| **Accuracy Improvement** | 85% → 97% (+12 points) | vivian-012 |
| **Hours Saved Annually** | 572 hours | vivian-012 |
| **Dashboards Created** | 5 for 15+ stakeholders | vivian-013 |
| **On-Time Delivery** | 100% over 6 months | vivian-013 |
| **Learning Speed** | pandas/NumPy in 2 weeks | vivian-017 |

---

## 🎯 ICG Data Analyst - Quick Prep

### **Top 5 Talking Points**
1. **Excel Expert (Level 5)**: 5 dashboards, 15+ stakeholders, 100% on-time
2. **Power BI Certified**: Microsoft Power BI Certification Training (The Knowledge Academy)
3. **Data Quality Pro**: 70% time reduction, 85%→97% accuracy improvement
4. **Fast Learner**: Learned pandas/NumPy in 2 weeks, Power BI certification completed
5. **Quantified Results**: 572 hours saved annually, 100% on-time delivery

### **Salary Negotiation**
- **Contract**: $500-600/day (open to adjustments after proving value)
- **Permanent**: $55k-70k/year (flexible based on learning opportunities)
- **Priority**: Mentorship and career growth over maximum compensation

### **Availability**
- **Start**: Immediate (2 weeks notice to current internship)
- **Work Rights**: Australian citizen (no visa required)
- **Hours**: Full-time 40 hrs/week available
- **Study**: Bachelor's until June 2026 (evening/weekend classes only)

---

## 📁 Important Files

| File | Purpose |
|------|---------|
| `vivian_profile_query.py` | **Query your professional profile** |
| `data/vivian_professional_profile.json` | 27 profile vectors (source data) |
| `UPLOAD_SUCCESS_SUMMARY.md` | Full upload documentation |
| `VIVIAN_PROFILE_SUMMARY.md` | Original 6000+ word profile |
| `PROFILE_UPLOAD_GUIDE.md` | Step-by-step upload guide |

---

## 🔧 Troubleshooting

### **Issue**: No results for professional queries
**Solution**: 
```bash
# Verify profile vectors exist
python3 -c "
from upstash_vector import Index
from dotenv import load_dotenv
load_dotenv()
index = Index.from_env()
results = index.query(data='Vivian Pham', top_k=5, include_metadata=True)
for r in results:
    if r.id.startswith('vivian'):
        print(f'✅ Found: {r.id} - {r.metadata.get(\"name\", \"N/A\")}')
"
```

### **Issue**: Food items in results instead of profile
**Solution**: Use `vivian_profile_query.py` instead of `rag_api.py`
- `rag_api.py` → Food queries
- `vivian_profile_query.py` → Professional profile queries

### **Issue**: Want to update profile
**Solution**:
1. Edit `data/vivian_professional_profile.json`
2. Run: `python3 upload_vivian_profile_to_upstash.py`
3. Upsert will update existing vectors automatically

---

## 🎓 Interview Practice Workflow

### **Daily Practice (15-20 min)**
```bash
# Run interactive mode
cd /Users/DELL/ragfood
python3 vivian_profile_query.py

# Practice 5-10 questions from different categories:
# 1. Technical skills question
# 2. Project/STAR format question
# 3. Behavioral question
# 4. Compensation question
# 5. Career goals question
```

### **Before Interview (1 hour)**
```bash
# Query top 10 likely questions
python3 vivian_profile_query.py "Tell me about yourself"
python3 vivian_profile_query.py "What are your Excel skills?"
python3 vivian_profile_query.py "Why do you want this role?"
python3 vivian_profile_query.py "Tell me about a time you learned something quickly"
python3 vivian_profile_query.py "What's your biggest strength?"
# ... etc
```

### **During Recruiter Call**
Keep terminal open with `vivian_profile_query.py` running:
- Recruiter asks: "What's your salary expectation?"
- You type query while talking
- Get instant accurate answer
- Respond confidently!

---

## 💡 Pro Tips

1. **Favorite the Interactive Mode**:
   ```bash
   alias vprofile='cd /Users/DELL/ragfood && python3 vivian_profile_query.py'
   ```
   Then just type: `vprofile`

2. **Save Common Queries**:
   Create `common_queries.txt`:
   ```
   What are my salary expectations?
   Do I have Power BI certification?
   Tell me about my Excel skills
   What data quality projects have I worked on?
   ```

3. **Practice STAR Variations**:
   - "Tell me about a data quality project"
   - "Describe a time you automated a process"
   - "Give me an example of improving accuracy"
   - All hit the same vector (vivian-012) with different phrasing!

---

## 📞 Support

**Questions?**
- Read: `UPLOAD_SUCCESS_SUMMARY.md` (full documentation)
- Check: `PROFILE_UPLOAD_GUIDE.md` (step-by-step guide)
- Review: `agents.md` (technical architecture)

**Issues?**
- Test connection: `python3 check_upstash_database.py`
- Verify JSON: `python3 -m json.tool data/vivian_professional_profile.json`
- Re-upload: `python3 upload_vivian_profile_to_upstash.py`

---

**🎉 Your professional digital twin is ready! Good luck with ICG!** 🚀

---

**Quick Access**:
- Repository: https://github.com/VivianP05/ragfood
- Profile: `/Users/DELL/ragfood/mydigitaltwin/VIVIAN_PROFILE_SUMMARY.md`
- Database: Upstash Vector (free-loon-62438)
- Vectors: 227 total (200 food + 27 professional)
