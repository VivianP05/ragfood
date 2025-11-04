"use server";

import { exec } from "child_process";
import { promisify } from "util";

const execPromise = promisify(exec);

/**
 * Digital Twin Profile Actions
 * Query Vivian's professional profile using RAG system
 */

export interface ProfileQueryResult {
  success: boolean;
  question: string;
  answer?: string;
  sources?: Array<{
    id: string;
    name: string;
    section: string;
    relevance: string;
  }>;
  profile_vectors_found?: number;
  error?: string;
}

/**
 * Query Vivian's professional profile using the Python RAG system
 */
export async function queryDigitalTwin(question: string): Promise<ProfileQueryResult> {
  try {
    if (!question || question.trim().length === 0) {
      return {
        success: false,
        question: question,
        error: "Question cannot be empty"
      };
    }

    // Execute Python script to query professional profile
    const scriptPath = "/Users/DELL/ragfood/vivian_profile_query.py";
    const { stdout, stderr } = await execPromise(
      `python3 "${scriptPath}" "${question.replace(/"/g, '\\"')}"`
    );

    if (stderr && stderr.trim().length > 0) {
      console.error("Python script stderr:", stderr);
    }

    // Parse JSON response from Python script
    const result = JSON.parse(stdout.trim());

    if (!result.success) {
      return {
        success: false,
        question: question,
        error: result.error || "Failed to query digital twin profile"
      };
    }

    return {
      success: true,
      question: question,
      answer: result.answer,
      sources: result.sources || [],
      profile_vectors_found: result.profile_vectors_found || 0
    };

  } catch (error) {
    console.error("Digital Twin Query Error:", error);
    return {
      success: false,
      question: question,
      error: error instanceof Error ? error.message : "Unknown error occurred"
    };
  }
}

/**
 * Get specific information about Vivian's skills
 */
export async function getSkillInformation(skillName: string): Promise<ProfileQueryResult> {
  const question = `What are my ${skillName} skills and achievements?`;
  return await queryDigitalTwin(question);
}

/**
 * Get Vivian's work experience
 */
export async function getWorkExperience(company?: string): Promise<ProfileQueryResult> {
  const question = company 
    ? `Tell me about my work experience at ${company}`
    : "What is my work experience and employment history?";
  return await queryDigitalTwin(question);
}

/**
 * Get Vivian's education background
 */
export async function getEducation(): Promise<ProfileQueryResult> {
  const question = "What is my educational background and qualifications?";
  return await queryDigitalTwin(question);
}

/**
 * Get Vivian's certifications
 */
export async function getCertifications(): Promise<ProfileQueryResult> {
  const question = "What certifications do I have?";
  return await queryDigitalTwin(question);
}

/**
 * Get Vivian's projects and achievements
 */
export async function getProjects(projectType?: string): Promise<ProfileQueryResult> {
  const question = projectType
    ? `Tell me about my ${projectType} projects and achievements`
    : "What are my key projects and achievements?";
  return await queryDigitalTwin(question);
}
