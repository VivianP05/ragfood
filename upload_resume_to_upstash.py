#!/usr/bin/env python3
"""
Upload Vivian's Resume to Upstash Vector Database

This script parses Vivian Pham's comprehensive resume and uploads it to Upstash Vector
for RAG-based resume question answering. The resume is chunked into semantic sections:
- Professional Summary
- Work Experience (Ausbiz, Jung Talents, Data Coaching)
- Technical Skills (Excel, Tableau, Power BI, Python, SQL, AI/ML)
- Projects (ragfood AI system)
- Education & Certifications
- Key Achievements & Metrics
- Career Goals
- Work Preferences

The script uses Upstash Vector's auto-embedding feature with the mxbai-embed-large-v1 model.

Usage:
    python3 upload_resume_to_upstash.py

Environment Variables Required:
    UPSTASH_VECTOR_REST_URL - Your Upstash Vector database URL
    UPSTASH_VECTOR_REST_TOKEN - Your Upstash Vector authentication token

Author: Vivian Pham
Date: November 19, 2025
"""

import os
import sys
from typing import List, Dict, Tuple
from dotenv import load_dotenv
from upstash_vector import Index

# Load environment variables
load_dotenv()

# Verify environment variables
if not os.getenv("UPSTASH_VECTOR_REST_URL") or not os.getenv("UPSTASH_VECTOR_REST_TOKEN"):
    print("❌ ERROR: Missing environment variables!")
    print("Please set UPSTASH_VECTOR_REST_URL and UPSTASH_VECTOR_REST_TOKEN in .env file")
    sys.exit(1)


def create_resume_chunks() -> List[Tuple[str, str, Dict]]:
    """
    Create semantic chunks from Vivian's resume for vector search.
    
    Each chunk represents a logical section of the resume with relevant metadata
    for better search and retrieval in the RAG system.
    
    Returns:
        List of tuples (id, text, metadata) ready for upsertion
    """
    chunks = []
    
    # 1. PROFESSIONAL SUMMARY
    chunks.append((
        "resume-summary",
        """Vivian Pham - Professional Summary
        
AI Data Analyst | Business Intelligence Specialist | Data Visualization Expert

Results-driven AI Data Analyst with proven expertise in Excel (Level 5), Tableau (Level 3), Power BI (Level 3), and Python automation. Demonstrated ability to deliver 70% time reduction and 97% accuracy improvement through data quality automation. Expert in building executive dashboards that save 144+ hours annually and serve 15+ stakeholders. Strong foundation in AI/ML technologies with hands-on RAG system development. Passionate about transforming data into actionable insights and driving business decisions through analytics.

Location: Sydney, Australia
Citizenship: Vietnamese - Unrestricted Australian work rights
Contact: GitHub.com/VivianP05

Key Achievements:
- 572 hours saved annually through Python data automation
- 97% data accuracy achieved (up from 85%)
- 15+ stakeholders using executive dashboards
- 100% on-time delivery record over 6 months
- Dual BI platform expertise - Tableau & Power BI""",
        {
            "section": "summary",
            "type": "overview",
            "location": "Sydney, Australia",
            "citizenship": "Vietnamese - Australian work rights",
            "expertise": "Excel Level 5, Tableau Level 3, Power BI Level 3, Python, AI/ML",
            "key_metrics": "572hrs saved, 97% accuracy, 15+ stakeholders, 100% on-time"
        }
    ))
    
    # 2. AUSBIZ CONSULTING EXPERIENCE
    chunks.append((
        "resume-ausbiz",
        """AI Data Analyst Intern | Ausbiz Consulting | Sydney, Australia
September 2025 - Present (3 months)

Data Quality & Automation:
- Automated data cleaning workflows achieving 70% time reduction (15h → 4h per week)
- Improved data accuracy from 85% to 97% through Python automation (pandas, NumPy)
- Process 50,000 records daily with automated validation rules
- Reduced critical errors by 90% (5% → 0.5%)
- Impact: 572 hours saved annually, enabled 2 additional client accounts

Dashboard Development:
- Built 5 executive dashboards in Excel used by 15+ stakeholders
- Reduced monthly reporting time by 60% (10h → 4h), saving 72 hours annually
- Maintained 100% on-time delivery record over 6 months
- Achieved 9/10 stakeholder satisfaction rating

Collaboration & Training:
- Trained 2 junior analysts on automation workflows
- Collaborated with senior analysts on client data quality projects
- Presented monthly insights to practice leadership

Technologies: Python, pandas, NumPy, Excel Advanced, VBA, Pivot Tables, Data Visualization""",
        {
            "section": "experience",
            "company": "Ausbiz Consulting",
            "position": "AI Data Analyst Intern",
            "location": "Sydney, Australia",
            "duration": "September 2025 - Present (3 months)",
            "skills": "Python, pandas, NumPy, Excel, VBA, Data Automation",
            "achievements": "70% time reduction, 97% accuracy, 572hrs saved annually",
            "stakeholders": "15+",
            "type": "current_role"
        }
    ))
    
    # 3. JUNG TALENTS EXPERIENCE
    chunks.append((
        "resume-jung-talents",
        """Data Dashboard Analyst | Jung Talents | Remote
5 months experience

Dual BI Platform Development:
- Completed comprehensive Data Dashboard project using both Tableau and Power BI
- Built end-to-end BI solutions from data connection to executive visualizations
- Implemented Power Query for ETL and data transformation
- Developed strategic platform selection expertise:
  * Tableau: Exploratory analytics, storytelling, LOD expressions
  * Power BI: Microsoft ecosystem integration, automated reporting

Technical Skills Developed:
- Tableau: Interactive dashboards, filters, parameters, calculated fields, data blending, heat maps, geographic visualizations, stories and presentations
- Power BI: DAX formulas, data modeling, relationships, star schema, interactive filters
- Data Modeling: Best practices for performance optimization and scalability

Business Impact:
- Translated business requirements into technical dashboard solutions
- Presented data insights to non-technical stakeholders
- Worked with real-world datasets across multiple business scenarios

Technologies: Tableau (Level 3), Power BI (Level 3), Power Query, DAX, SQL, Excel""",
        {
            "section": "experience",
            "company": "Jung Talents",
            "position": "Data Dashboard Analyst",
            "location": "Remote",
            "duration": "5 months",
            "skills": "Tableau Level 3, Power BI Level 3, Power Query, DAX, SQL",
            "focus": "Dual BI platform expertise, dashboard development, stakeholder communication",
            "achievements": "End-to-end BI solutions, LOD expressions, data modeling",
            "type": "previous_role"
        }
    ))
    
    # 4. DATA COACHING EXPERIENCE
    chunks.append((
        "resume-data-coaching",
        """AI Data Analyst Intern | Data Coaching | Melbourne, Australia
May 2025 - August 2025 (4 months)

Executive Dashboard Design:
- Designed and deployed KPI dashboard for 15 stakeholders across 3 departments
- Achieved 100% adoption rate with 9/10 average rating
- Reduced report preparation time by 60% (10h → 4h monthly)
- Built 12 KPIs across 4 categories: data quality, efficiency, productivity, satisfaction

Stakeholder Management:
- Interviewed 5 senior stakeholders for requirements gathering
- Delivered 2 group training sessions for 15 users
- Presented monthly insights to senior leadership (15-20 min presentations)
- Template reused for 3 additional client dashboards

Technologies: Excel Advanced, VBA Macros, Pivot Tables, Advanced Formulas, Data Visualization""",
        {
            "section": "experience",
            "company": "Data Coaching",
            "position": "AI Data Analyst Intern",
            "location": "Melbourne, Australia",
            "duration": "May 2025 - August 2025 (4 months)",
            "skills": "Excel Advanced, VBA, Pivot Tables, Dashboard Design",
            "achievements": "100% adoption, 9/10 rating, 60% time reduction",
            "stakeholders": "15 across 3 departments",
            "type": "previous_role"
        }
    ))
    
    # 5. RAGFOOD PROJECT
    chunks.append((
        "resume-ragfood-project",
        """ragfood - AI Food Recommendation System | Personal Project
September 2025 - November 2025
Live Demo: https://ragfood.vercel.app | GitHub: https://github.com/VivianP05/ragfood

Full-Stack RAG Application:
- Built production-ready RAG (Retrieval-Augmented Generation) system with 200 food vectors
- Achieved 0.7-1.5 second average query response time
- Frontend: Next.js 16, TypeScript, React 19, Tailwind CSS
- Backend: Python, Upstash Vector (mxbai-embed-large-v1), Groq AI (llama-3.1-8b-instant)
- Deployment: Live on Vercel with full CI/CD pipeline

Impact: Demonstrates hands-on AI/ML expertise, full-stack development skills, and ability to learn 4 new technologies in 3 months.

Technologies: Next.js 16, React 19, TypeScript, Python, Upstash Vector, Groq AI, Tailwind CSS, Vercel""",
        {
            "section": "projects",
            "project": "ragfood",
            "type": "AI/ML RAG System",
            "url": "https://ragfood.vercel.app",
            "github": "https://github.com/VivianP05/ragfood",
            "duration": "September 2025 - November 2025",
            "tech_stack": "Next.js 16, React 19, TypeScript, Python, Upstash Vector, Groq AI",
            "achievements": "Production deployment, 0.7-1.5s response time, 200 vectors",
            "learning": "4 new technologies in 3 months"
        }
    ))
    
    # 6. EXCEL SKILLS
    chunks.append((
        "resume-excel-skills",
        """Excel Skills - Level 5 (Expert)

Proficiency: Level 5 (Expert) - 5 years experience
- Advanced formulas: XLOOKUP, INDEX-MATCH, complex nested formulas
- VBA Macros: Automation scripts, custom functions
- Pivot Tables: Complex multi-dimensional analysis
- Data Visualization: Professional dashboards and charts
- Power Query: Data transformation and ETL

Achievements:
- Built 5 executive dashboards used by 15+ stakeholders
- Saved 72 hours annually through Excel automation
- Achieved 9/10 stakeholder satisfaction rating
- 100% on-time delivery record over 6 months
- Reduced monthly reporting time by 60% (10h → 4h)

Real-world Applications:
- Executive KPI dashboards for 15 stakeholders across 3 departments
- Automated data quality validation for 50,000 daily records
- Financial modeling and forecasting templates
- Client reporting automation""",
        {
            "section": "technical_skills",
            "skill": "Excel",
            "level": "5",
            "proficiency": "Expert",
            "experience": "5 years",
            "capabilities": "VBA, Pivot Tables, XLOOKUP, INDEX-MATCH, Power Query",
            "achievements": "5 dashboards, 72hrs saved annually, 15+ stakeholders",
            "type": "core_strength"
        }
    ))
    
    # 7. TABLEAU SKILLS
    chunks.append((
        "resume-tableau-skills",
        """Tableau Skills - Level 3 (Intermediate)

Proficiency: Level 3 (Intermediate) - 5 months hands-on experience at Jung Talents
- Interactive dashboards with filters, parameters, and calculated fields
- LOD (Level of Detail) expressions for advanced calculations
- Data blending from multiple sources
- Heat maps, geographic visualizations, and KPI cards
- Stories and presentations for stakeholder communication
- Dashboard design and performance optimization best practices

Experience:
- 5-month intensive Data Dashboard project at Jung Talents
- Built executive-level BI visualizations
- Real-world business analytics scenarios
- Exploratory analytics and storytelling

Focus Areas:
- Business intelligence and executive reporting
- Interactive data exploration
- Visual storytelling for non-technical audiences""",
        {
            "section": "technical_skills",
            "skill": "Tableau",
            "level": "3",
            "proficiency": "Intermediate",
            "experience": "5 months at Jung Talents",
            "capabilities": "Interactive dashboards, LOD expressions, data blending, storytelling",
            "focus": "Business intelligence, executive reporting, visual storytelling",
            "type": "bi_tool"
        }
    ))
    
    # 8. POWER BI SKILLS
    chunks.append((
        "resume-power-bi-skills",
        """Power BI Skills - Level 3 (Intermediate)

Proficiency: Level 3 (Intermediate) - Microsoft Certified + 5 months Jung Talents experience
- DAX formulas for advanced calculations and measures
- Power Query for ETL and data transformation
- Data modeling: Relationships, star schema, optimization
- Interactive dashboards with slicers and filters
- Row-level security and data governance
- Microsoft ecosystem integration

Experience:
- Microsoft Power BI Certification Training (The Knowledge Academy)
- 5-month Data Dashboard project at Jung Talents
- Practical hands-on project experience with real datasets
- Automated reporting and scheduled refreshes

Focus Areas:
- Microsoft ecosystem integration
- Automated reporting and BI solutions
- Enterprise data modeling
- End-to-end BI development""",
        {
            "section": "technical_skills",
            "skill": "Power BI",
            "level": "3",
            "proficiency": "Intermediate",
            "experience": "Microsoft Certified + 5 months Jung Talents",
            "capabilities": "DAX, Power Query, data modeling, star schema, automation",
            "certification": "Microsoft Power BI Certification Training",
            "focus": "Microsoft integration, automated reporting, enterprise BI",
            "type": "bi_tool"
        }
    ))
    
    # 9. PYTHON SKILLS
    chunks.append((
        "resume-python-skills",
        """Python Programming - Level 3 (Intermediate)

Proficiency: Level 3 (Intermediate) - Data analysis and automation focus
- pandas (Level 4): DataFrames, data cleaning, 250k records processed
- NumPy: Numerical computations and array operations
- Jupyter Notebooks: Interactive analysis and documentation
- Data automation: Workflow scripting, scheduled jobs
- API integration: REST APIs, JSON handling

Achievements:
- Automated data cleaning achieving 70% time reduction (15h → 4h per week)
- Improved data accuracy from 85% to 97%
- Process 50,000 records daily with automated validation
- Saved 572 hours annually through Python automation
- Built production RAG system with Upstash Vector and Groq AI

Real-world Applications:
- Data quality automation at Ausbiz Consulting
- Full-stack RAG application (ragfood project)
- ETL pipelines and data transformation
- Automated reporting and analytics""",
        {
            "section": "technical_skills",
            "skill": "Python",
            "level": "3",
            "proficiency": "Intermediate",
            "libraries": "pandas Level 4, NumPy, Jupyter",
            "achievements": "70% time reduction, 97% accuracy, 572hrs saved annually",
            "applications": "Data automation, RAG systems, ETL pipelines",
            "type": "programming"
        }
    ))
    
    # 10. AI/ML SKILLS
    chunks.append((
        "resume-ai-ml-skills",
        """AI/ML & Cloud Technologies

Vector Databases:
- Upstash Vector (Level 3): Semantic search, 200 vectors, 1024 dimensions
- mxbai-embed-large-v1 embeddings for text vectorization
- Cosine similarity scoring and relevance ranking

LLM Integration:
- Groq AI (Level 2): RAG architecture, prompt engineering
- llama-3.1-8b-instant model integration
- Chat completions and streaming responses

Cloud Platforms:
- Vercel deployment and CI/CD
- Environment management and secrets
- Production monitoring

Real-world Projects:
- ragfood: Production RAG system with 200 food vectors
- Response time: 0.7-1.5 seconds average
- Full-stack: Next.js 16 + Python + Upstash + Groq
- Learned 4 new technologies in 3 months

Technologies: Upstash Vector, Groq AI, LLMs, RAG architecture, embeddings, semantic search""",
        {
            "section": "technical_skills",
            "category": "AI/ML",
            "skills": "Vector databases, LLM integration, RAG systems, embeddings",
            "tools": "Upstash Vector, Groq AI, llama-3.1-8b-instant",
            "projects": "ragfood production system",
            "achievements": "200 vectors, 0.7-1.5s response time, 4 new tech in 3 months",
            "type": "emerging_tech"
        }
    ))
    
    # 11. SOFT SKILLS
    chunks.append((
        "resume-soft-skills",
        """Soft Skills & Professional Competencies

Problem-Solving - Level 5 (Expert):
- Systematic root cause analysis
- Achieved 70% efficiency gains through process improvement
- Data-driven decision making

Learning Agility - Level 5 (Expert):
- Learned pandas/NumPy in 2 weeks for Ausbiz role
- Mastered 4 new technologies in 3 months (Next.js, TypeScript, Upstash, Groq)
- Self-taught full-stack RAG development

Time Management - Level 5 (Expert):
- 100% on-time delivery record over 6 months
- Balancing full-time study + internships + personal projects
- Consistently meet deadlines while maintaining quality

Communication - Level 4 (Advanced):
- Monthly stakeholder presentations (15-20 minutes)
- Trained 2 junior analysts on automation workflows
- Translate complex data insights to non-technical audiences
- Interviewed 5 senior stakeholders for requirements gathering

Collaboration - Level 4 (Advanced):
- Cross-functional team experience (3 departments)
- Trained 2 analysts, supported 15+ stakeholders
- Senior analyst collaboration on client projects""",
        {
            "section": "soft_skills",
            "key_strengths": "Problem-solving Level 5, Learning Agility Level 5, Time Management Level 5",
            "achievements": "100% on-time delivery, trained 2 analysts, 15+ stakeholders",
            "evidence": "70% efficiency gains, 4 new tech in 3 months, monthly presentations",
            "type": "professional_competencies"
        }
    ))
    
    # 12. EDUCATION & CERTIFICATIONS
    chunks.append((
        "resume-education",
        """Education & Professional Certifications

Bachelor of Information Systems Management
Victoria University | Melbourne, Australia
Graduating: June 2026
Current GPA: [GPA if available]

Master of Data Science (Planned)
Commencing: July 2026 (after graduation)
Focus: Advanced analytics, machine learning, AI systems

Professional Certifications:
- Microsoft Power BI Certification Training - The Knowledge Academy (Completed)
- [Other certifications if any]

Academic Focus:
- Information Systems Management
- Data Analytics and Business Intelligence
- Database Management and SQL
- Programming and Software Development""",
        {
            "section": "education",
            "degree": "Bachelor of Information Systems Management",
            "university": "Victoria University",
            "location": "Melbourne, Australia",
            "graduation": "June 2026",
            "future_plans": "Master of Data Science starting July 2026",
            "certifications": "Microsoft Power BI",
            "type": "academic_background"
        }
    ))
    
    # 13. KEY ACHIEVEMENTS & METRICS
    chunks.append((
        "resume-achievements",
        """Key Achievements & Quantified Metrics

Efficiency & Automation:
- 572 hours saved annually through Python data automation
- 72 hours saved annually through Excel dashboard automation
- 70% time reduction in data cleaning workflows (15h → 4h per week)
- 60% time reduction in monthly reporting (10h → 4h per month)

Quality & Accuracy:
- 97% data accuracy achieved (improved from 85%)
- 90% error reduction - critical errors from 5% to 0.5%
- 100% on-time delivery record over 6 months
- 9/10 stakeholder satisfaction rating on dashboard quality

Scale & Impact:
- 50,000 records automated daily
- 15+ stakeholders using dashboards
- 5 executive dashboards built and deployed
- 2 additional client accounts enabled without hiring
- 644 total hours saved annually (572 + 72)

Business Value:
- Enabled 2 additional client accounts through efficiency gains
- 100% dashboard adoption rate across 3 departments
- Template reused for 3 additional client dashboards
- Trained 2 junior analysts, multiplying impact""",
        {
            "section": "achievements",
            "total_hours_saved": "644 hours annually",
            "accuracy_improvement": "85% → 97%",
            "stakeholder_impact": "15+ stakeholders, 9/10 rating",
            "delivery_record": "100% on-time over 6 months",
            "scale": "50,000 daily records, 5 dashboards",
            "type": "quantified_results"
        }
    ))
    
    # 14. CAREER GOALS
    chunks.append((
        "resume-career-goals",
        """Career Goals & Aspirations

Short-term Goals (2025-2026):
- Complete Bachelor's degree in Information Systems Management (June 2026)
- Gain real-world AI/ML experience in data analytics roles
- Develop advanced proficiency in Tableau and Power BI
- Build portfolio of impactful data projects

Long-term Goals (2026+):
- Pursue Master of Data Science (starting July 2026)
- Progress to Data Scientist or Senior Data Analyst role
- Work on impactful ML and advanced analytics projects

Target Companies:
Tech Companies:
- Canva, Atlassian, REA Group, Seek

Consulting Firms:
- Deloitte Digital, PwC Analytics, KPMG, Accenture Applied Intelligence

Focus Areas:
- Impactful ML and data analytics projects
- Advanced business intelligence and visualization
- AI-powered decision support systems
- End-to-end data solutions

Values:
- Learning opportunities and mentorship over maximum salary
- Challenging projects with real business impact
- Strong data science culture and collaboration
- Innovation and cutting-edge technologies""",
        {
            "section": "career_goals",
            "short_term": "Complete degree June 2026, gain AI/ML experience",
            "long_term": "Master's degree, Data Scientist role",
            "target_companies": "Canva, Atlassian, Deloitte Digital, PwC, KPMG",
            "focus": "AI/ML projects, advanced BI, decision support systems",
            "type": "aspirations"
        }
    ))
    
    # 15. COMPENSATION & AVAILABILITY
    chunks.append((
        "resume-compensation",
        """Compensation Expectations & Availability

Compensation Expectations:
Permanent Roles: $55,000 - $70,000 AUD annually
- Entry-level Data Analyst: $55k - $65k
- Junior BI Analyst: $60k - $70k

Contract Roles: $500 - $600 per day
- Open to rate adjustments after proving value (1-3 months)

Priority: Learning opportunities, mentorship, and challenging projects over maximum salary

Availability:
- Work Authorization: Vietnamese Citizen - Unrestricted Australian work rights (no visa required)
- Start Date: Immediate start (2 weeks notice to current role)
- Capacity: Full-time, 40 hours per week
- Study Commitment: Evening/weekend classes only (until June 2026)

Work Arrangement Preferences:
- Preferred: Hybrid (3 days office, 2 days remote)
- Open to: Fully remote or full-time office
- Remote Experience: Proven track record with self-directed work
- Travel: Willing to travel 10-15% (1-2 trips per month)

Location Flexibility:
- Currently: Sydney, Australia
- Willing to relocate: Melbourne, Brisbane, Canberra
- Notice period: 1-2 months for relocation
- Relocation assistance preferred but not required""",
        {
            "section": "compensation_availability",
            "permanent_salary": "$55,000 - $70,000 AUD",
            "contract_rate": "$500 - $600 per day",
            "work_authorization": "Vietnamese Citizen - Unrestricted Australian rights",
            "availability": "Immediate (2 weeks notice)",
            "work_arrangement": "Hybrid preferred, remote or office flexible",
            "location": "Sydney, open to Melbourne/Brisbane/Canberra",
            "type": "logistics"
        }
    ))
    
    print(f"✅ Created {len(chunks)} resume chunks")
    return chunks


def upload_to_upstash(vectors: List[Tuple[str, str, Dict]]) -> Dict:
    """
    Upload resume vectors to Upstash Vector database.
    
    Args:
        vectors: List of tuples (id, text, metadata)
        
    Returns:
        Dictionary with upload statistics
    """
    try:
        # Initialize Upstash Vector index
        print("\n📡 Connecting to Upstash Vector database...")
        index = Index.from_env()
        print("✅ Connected successfully")
        
        # Upload vectors (auto-embedding enabled)
        print(f"\n📤 Uploading {len(vectors)} resume chunks...")
        print("   (Upstash will auto-embed using mxbai-embed-large-v1 model)")
        
        # Upsert vectors to database
        result = index.upsert(vectors=vectors)
        
        print("✅ Upload complete!")
        print(f"   Uploaded: {len(vectors)} resume vectors")
        
        return {
            "success": True,
            "uploaded_count": len(vectors),
            "result": result
        }
        
    except Exception as e:
        print(f"❌ ERROR during upload: {e}")
        print(f"Error type: {type(e).__name__}")
        return {
            "success": False,
            "error": str(e)
        }


def test_resume_queries():
    """
    Test the uploaded resume with sample queries.
    """
    try:
        print("\n🧪 TESTING RESUME QUERIES")
        print("=" * 80)
        
        index = Index.from_env()
        
        test_queries = [
            "What is Vivian's experience with Tableau?",
            "Tell me about Jung Talents experience",
            "What are Vivian's Power BI skills?",
            "What data automation achievements does Vivian have?",
            "What are Vivian's salary expectations?",
            "What Excel skills does Vivian have?",
            "What AI/ML experience does Vivian have?",
            "What are Vivian's career goals?",
            "Is Vivian available for full-time work?",
            "What soft skills does Vivian have?"
        ]
        
        for query in test_queries:
            print(f"\n📝 Query: '{query}'")
            
            results = index.query(
                data=query,
                top_k=3,
                include_metadata=True
            )
            
            print(f"✅ Found {len(results)} relevant resume sections:\n")
            
            for i, result in enumerate(results, 1):
                metadata = result.metadata
                print(f"   {i}. Score: {result.score:.4f}")
                print(f"      ID: {result.id}")
                print(f"      Section: {metadata.get('section', 'N/A')}")
                
                # Show relevant metadata based on section
                if metadata.get('company'):
                    print(f"      Company: {metadata.get('company')}")
                if metadata.get('skill'):
                    print(f"      Skill: {metadata.get('skill')} (Level {metadata.get('level', 'N/A')})")
                if metadata.get('achievements'):
                    print(f"      Key Achievement: {metadata.get('achievements', 'N/A')[:60]}...")
                print()
            
            print("-" * 80)
        
    except Exception as e:
        print(f"❌ ERROR during testing: {e}")


def main():
    """
    Main execution function.
    """
    print("=" * 80)
    print("🚀 Vivian's Resume Upload to Upstash Vector")
    print("=" * 80)
    print()
    
    # Step 1: Create resume chunks
    print("📝 STEP 1: Creating semantic resume chunks...")
    chunks = create_resume_chunks()
    
    # Print statistics
    sections = {}
    for chunk_id, text, metadata in chunks:
        section = metadata.get("section", "unknown")
        sections[section] = sections.get(section, 0) + 1
    
    print("\n📊 Resume Statistics:")
    print(f"   Total chunks: {len(chunks)}")
    print(f"   Sections breakdown:")
    for section, count in sorted(sections.items()):
        print(f"      - {section}: {count} chunks")
    print()
    
    # Step 2: Upload to Upstash
    print("📤 STEP 2: Uploading to Upstash Vector...")
    upload_result = upload_to_upstash(chunks)
    print()
    
    if not upload_result["success"]:
        print("❌ Upload failed. Exiting...")
        sys.exit(1)
    
    # Step 3: Test queries
    print("🧪 STEP 3: Testing resume queries...")
    test_resume_queries()
    
    # Final summary
    print()
    print("=" * 80)
    print("✅ RESUME UPLOAD COMPLETE!")
    print("=" * 80)
    print()
    print("📊 Summary:")
    print(f"   ✓ Uploaded: {upload_result['uploaded_count']} resume chunks")
    print(f"   ✓ Sections: Summary, Experience (3), Projects, Skills (6), Education, Goals")
    print(f"   ✓ Embedding model: mxbai-embed-large-v1 (1024 dimensions)")
    print(f"   ✓ Database: Upstash Vector (free-loon-62438)")
    print()
    print("🎯 Your Resume RAG is now ready for:")
    print("   • Recruiter questions about experience, skills, compensation")
    print("   • Interview preparation (Tableau, Power BI, Jung Talents, Ausbiz)")
    print("   • Career goals and availability questions")
    print("   • Technical skills assessment (Excel Level 5, BI tools, Python, AI/ML)")
    print()
    print("🚀 Next Steps:")
    print("   1. Test resume queries: python3 digital_twin_rag.py")
    print("   2. Ask about Jung Talents: 'Tell me about Jung Talents experience'")
    print("   3. Ask about skills: 'What are Vivian's Tableau skills?'")
    print("   4. Ask about compensation: 'What are salary expectations?'")
    print()
    print("💡 Sample questions to try:")
    print("   • 'What is Vivian's Tableau and Power BI experience?'")
    print("   • 'Tell me about the Jung Talents Data Dashboard project'")
    print("   • 'What data automation achievements does Vivian have?'")
    print("   • 'What are Vivian's Excel skills and level?'")
    print("   • 'Is Vivian available for full-time work?'")
    print("   • 'What are Vivian's career goals and target companies?'")
    print()


if __name__ == "__main__":
    main()
