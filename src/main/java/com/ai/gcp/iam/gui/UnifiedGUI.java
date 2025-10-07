package com.ai.gcp.iam.gui;

import java.awt.BorderLayout;
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;

import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.JScrollPane;
import javax.swing.JTextArea;
import javax.swing.SwingUtilities;

import com.ai.gcp.iam.repository.IAMRepository;

public class UnifiedGUI extends JFrame {

	private static final long serialVersionUID = 1L;

	private IAMRepository repo;

	public UnifiedGUI() {
		repo = new IAMRepository();
		setTitle("GCP IAM Management");
		setSize(600, 500);
		setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		setLayout(new BorderLayout());

		JButton btnSync = new JButton("Sync IAM from GCP");
		JTextArea textArea = new JTextArea();
		add(new JScrollPane(textArea), BorderLayout.CENTER);
		add(btnSync, BorderLayout.SOUTH);

		btnSync.addActionListener(e -> {
			textArea.setText("Syncing IAM users and AI alerts...\n");

			SwingUtilities.invokeLater(() -> {
				// ---------- Try connecting to Python backend ----------
				try {
					String projectId = "demo-project"; // for dummy/demo mode
					URL url = new URL("http://127.0.0.1:5000/iam/sync/" + projectId);
					HttpURLConnection conn = (HttpURLConnection) url.openConnection();
					conn.setConnectTimeout(3000); // 3 seconds timeout
					conn.setReadTimeout(5000);
					conn.setRequestMethod("GET");

					BufferedReader in = new BufferedReader(new InputStreamReader(conn.getInputStream()));
					String inputLine;
					StringBuilder response = new StringBuilder();
					while ((inputLine = in.readLine()) != null) {
						response.append(inputLine).append("\n");
					}
					in.close();

					textArea.append("✅ Backend API response received.\n");

				} catch (Exception ex) {
					textArea.append("⚠️ Cannot connect to Python backend. Using local MySQL data.\n");
					System.err.println("Backend connection error: " + ex.getMessage());
				}

				// ---------- Load latest users & AI alerts from MySQL ----------
				textArea.append("\n=== IAM Users ===\n");
				try {
					for (String user : repo.getAllUsers()) {
						textArea.append(user + "\n");
					}
				} catch (Exception ex) {
					textArea.append("Error fetching IAM users from MySQL: " + ex.getMessage() + "\n");
					ex.printStackTrace();
				}

				textArea.append("\n=== AI Alerts ===\n");
				try {
					for (String alert : repo.getAllAIAlerts()) {
						textArea.append(alert + "\n");
					}
				} catch (Exception ex) {
					textArea.append("Error fetching AI alerts from MySQL: " + ex.getMessage() + "\n");
					ex.printStackTrace();
				}
			});
		});
	}

	public static void main(String[] args) {
		SwingUtilities.invokeLater(() -> {
			new UnifiedGUI().setVisible(true);
		});
	}
}
