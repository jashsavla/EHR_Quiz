#!/usr/bin/env python3
"""
Test script to populate the database with sample data for dashboard testing
"""

import requests
import json
import time

# Sample data that matches the summaries structure
sample_submissions = [
    [
        {
            "prompt_text": "Patient Name: John Doe\nDate of Birth: 05/12/1985\nMedical History: Hypertension (diagnosed 2018), Type 2 Diabetes (diagnosed 2015)\nCurrent Medications: Lisinopril 10mg daily, Metformin 1000mg twice daily\nVital Signs: BP 130/80, HR 72, Temp 98.6°F\nChief Complaint: Follow-up for medication management\nAssessment: Both conditions well-controlled with current medication regimen.",
            "ai_summary": "John Doe (37M) with controlled hypertension and T2DM on Lisinopril and Metformin. Vitals stable. Medication regimen effective.",
            "rating": 4
        },
        {
            "prompt_text": "Patient Name: Jane Smith\nDate of Birth: 03/15/1990\nMedical History: Asthma (childhood onset), Seasonal Allergies\nCurrent Medications: Albuterol inhaler PRN, Fluticasone nasal spray daily\nVital Signs: BP 118/75, HR 68, Temp 98.4°F, O2 Sat 99%\nChief Complaint: Annual physical examination\nAssessment: Asthma well-controlled, no exacerbations in past year.",
            "ai_summary": "Jane Smith (33F) with well-controlled asthma and seasonal allergies. No recent asthma exacerbations. Current medication plan effective.",
            "rating": 5
        },
        {
            "prompt_text": "Patient Name: Robert Johnson\nDate of Birth: 09/28/1975\nMedical History: Coronary Artery Disease (CAD), Hyperlipidemia\nCurrent Medications: Atorvastatin 40mg daily, Aspirin 81mg daily, Metoprolol 25mg twice daily\nVital Signs: BP 125/78, HR 65, Temp 98.2°F\nChief Complaint: Routine cardiac follow-up\nAssessment: CAD stable, lipids at goal, good medication compliance.",
            "ai_summary": "Robert Johnson (48M) with stable CAD and controlled hyperlipidemia. On appropriate cardiac medications with good compliance. Vitals within normal range.",
            "rating": 3
        },
        {
            "prompt_text": "Patient Name: Maria Garcia\nDate of Birth: 11/03/1995\nMedical History: Migraine headaches, Anxiety\nCurrent Medications: Sumatriptan as needed, Sertraline 50mg daily\nVital Signs: BP 115/70, HR 75, Temp 98.8°F\nChief Complaint: Migraine frequency review\nAssessment: Migraines reduced in frequency with current preventive measures.",
            "ai_summary": "Maria Garcia (28F) reports decreased migraine frequency and well-controlled anxiety on current medication regimen. Vitals normal.",
            "rating": 4
        },
        {
            "prompt_text": "Patient Name: William Chen\nDate of Birth: 07/15/1980\nMedical History: Type 1 Diabetes, Hypothyroidism\nCurrent Medications: Insulin pump, Levothyroxine 100mcg daily\nVital Signs: BP 122/76, HR 70, Temp 98.4°F\nChief Complaint: Diabetes management review\nAssessment: Blood sugar levels well-controlled with insulin pump.",
            "ai_summary": "William Chen (43M) with T1DM managed via insulin pump and stable hypothyroidism. Good glycemic control and normal thyroid function.",
            "rating": 5
        }
    ],
    # Second submission with different ratings
    [
        {
            "prompt_text": "Patient Name: John Doe\nDate of Birth: 05/12/1985\nMedical History: Hypertension (diagnosed 2018), Type 2 Diabetes (diagnosed 2015)\nCurrent Medications: Lisinopril 10mg daily, Metformin 1000mg twice daily\nVital Signs: BP 130/80, HR 72, Temp 98.6°F\nChief Complaint: Follow-up for medication management\nAssessment: Both conditions well-controlled with current medication regimen.",
            "ai_summary": "John Doe (37M) with controlled hypertension and T2DM on Lisinopril and Metformin. Vitals stable. Medication regimen effective.",
            "rating": 3
        },
        {
            "prompt_text": "Patient Name: Jane Smith\nDate of Birth: 03/15/1990\nMedical History: Asthma (childhood onset), Seasonal Allergies\nCurrent Medications: Albuterol inhaler PRN, Fluticasone nasal spray daily\nVital Signs: BP 118/75, HR 68, Temp 98.4°F, O2 Sat 99%\nChief Complaint: Annual physical examination\nAssessment: Asthma well-controlled, no exacerbations in past year.",
            "ai_summary": "Jane Smith (33F) with well-controlled asthma and seasonal allergies. No recent asthma exacerbations. Current medication plan effective.",
            "rating": 4
        },
        {
            "prompt_text": "Patient Name: Robert Johnson\nDate of Birth: 09/28/1975\nMedical History: Coronary Artery Disease (CAD), Hyperlipidemia\nCurrent Medications: Atorvastatin 40mg daily, Aspirin 81mg daily, Metoprolol 25mg twice daily\nVital Signs: BP 125/78, HR 65, Temp 98.2°F\nChief Complaint: Routine cardiac follow-up\nAssessment: CAD stable, lipids at goal, good medication compliance.",
            "ai_summary": "Robert Johnson (48M) with stable CAD and controlled hyperlipidemia. On appropriate cardiac medications with good compliance. Vitals within normal range.",
            "rating": 2
        },
        {
            "prompt_text": "Patient Name: Maria Garcia\nDate of Birth: 11/03/1995\nMedical History: Migraine headaches, Anxiety\nCurrent Medications: Sumatriptan as needed, Sertraline 50mg daily\nVital Signs: BP 115/70, HR 75, Temp 98.8°F\nChief Complaint: Migraine frequency review\nAssessment: Migraines reduced in frequency with current preventive measures.",
            "ai_summary": "Maria Garcia (28F) reports decreased migraine frequency and well-controlled anxiety on current medication regimen. Vitals normal.",
            "rating": 5
        },
        {
            "prompt_text": "Patient Name: William Chen\nDate of Birth: 07/15/1980\nMedical History: Type 1 Diabetes, Hypothyroidism\nCurrent Medications: Insulin pump, Levothyroxine 100mcg daily\nVital Signs: BP 122/76, HR 70, Temp 98.4°F\nChief Complaint: Diabetes management review\nAssessment: Blood sugar levels well-controlled with insulin pump.",
            "ai_summary": "William Chen (43M) with T1DM managed via insulin pump and stable hypothyroidism. Good glycemic control and normal thyroid function.",
            "rating": 4
        }
    ]
]

def submit_test_data():
    """Submit test data to the API"""
    base_url = "http://localhost:5000"
    
    print("Submitting test data...")
    
    for i, submission in enumerate(sample_submissions, 1):
        try:
            response = requests.post(f"{base_url}/api/ratings", json=submission)
            if response.status_code == 201:
                print(f"✅ Submission {i} successful")
                time.sleep(1)  # Small delay between submissions
            else:
                print(f"❌ Submission {i} failed: {response.status_code}")
                print(response.text)
        except requests.exceptions.RequestException as e:
            print(f"❌ Error submitting {i}: {e}")
    
    print("\nFetching dashboard stats...")
    try:
        response = requests.get(f"{base_url}/api/ratings/stats")
        if response.status_code == 200:
            stats = response.json()
            print(f"✅ Dashboard data received")
            print(f"   Total sessions: {stats['overall_statistics']['total_sessions']}")
            print(f"   Total ratings: {stats['overall_statistics']['total_ratings']}")
            print(f"   Average rating: {stats['overall_statistics']['average_rating']:.2f}")
        else:
            print(f"❌ Failed to fetch stats: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Error fetching stats: {e}")

if __name__ == "__main__":
    submit_test_data()
