const corsHeaders = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
  "Access-Control-Allow-Headers":
    "Content-Type, Authorization, X-Client-Info, Apikey",
};

interface ConsultationSubmission {
  id: string;
  first_name: string;
  last_name: string;
  email: string;
  phone: string;
  interest: string;
  message: string;
  consultation_date: string;
  consultation_time: string;
  created_at: string;
}

function formatInterest(interest: string): string {
  const interestMap: Record<string, string> = {
    borrowing: "Borrowing: Private mortgage or construction financing",
    investing: "Investing: MIC investment opportunities",
    brokering: "Brokering: Partner with us",
  };
  return interestMap[interest] || interest;
}

function generateEmailHTML(submission: ConsultationSubmission): string {
  return `
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>New Consultation Request</title>
  <style>
    body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif; line-height: 1.6; color: #333; margin: 0; padding: 0; background-color: #f4f4f4; }
    .container { max-width: 600px; margin: 20px auto; background: #ffffff; border-radius: 8px; overflow: hidden; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }
    .header { background: linear-gradient(135deg, #0B1635 0%, #1a2845 100%); color: #ffffff; padding: 30px 20px; text-align: center; }
    .header h1 { margin: 0; font-size: 24px; font-weight: 600; }
    .header p { margin: 8px 0 0; font-size: 14px; opacity: 0.9; }
    .content { padding: 30px 20px; }
    .badge { display: inline-block; background: #ff6600; color: #ffffff; padding: 6px 12px; border-radius: 4px; font-size: 12px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 20px; }
    .section { margin-bottom: 25px; }
    .section-title { font-size: 14px; font-weight: 600; color: #666; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 12px; }
    .info-row { display: flex; padding: 12px 0; border-bottom: 1px solid #eee; }
    .info-label { font-weight: 600; color: #0B1635; min-width: 140px; }
    .info-value { color: #333; flex: 1; }
    .message-box { background: #f9f9f9; border-left: 3px solid #ff6600; padding: 16px; margin-top: 12px; border-radius: 4px; }
    .message-box p { margin: 0; color: #333; }
    .footer { background: #f9f9f9; padding: 20px; text-align: center; font-size: 12px; color: #666; }
    .footer a { color: #ff6600; text-decoration: none; }
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <h1>New Consultation Request</h1>
      <p>Richview Capital MIC</p>
    </div>
    <div class="content">
      <span class="badge">New Submission</span>

      <div class="section">
        <div class="section-title">Contact Information</div>
        <div class="info-row">
          <span class="info-label">Name:</span>
          <span class="info-value">${submission.first_name} ${submission.last_name}</span>
        </div>
        <div class="info-row">
          <span class="info-label">Email:</span>
          <span class="info-value"><a href="mailto:${submission.email}">${submission.email}</a></span>
        </div>
        <div class="info-row">
          <span class="info-label">Phone:</span>
          <span class="info-value"><a href="tel:${submission.phone}">${submission.phone}</a></span>
        </div>
      </div>

      <div class="section">
        <div class="section-title">Consultation Details</div>
        <div class="info-row">
          <span class="info-label">Interest:</span>
          <span class="info-value">${formatInterest(submission.interest)}</span>
        </div>
        <div class="info-row">
          <span class="info-label">Preferred Date:</span>
          <span class="info-value">${new Date(submission.consultation_date).toLocaleDateString('en-US', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' })}</span>
        </div>
        <div class="info-row">
          <span class="info-label">Preferred Time:</span>
          <span class="info-value">${submission.consultation_time}</span>
        </div>
      </div>

      <div class="section">
        <div class="section-title">Message</div>
        <div class="message-box">
          <p>${submission.message.replace(/\n/g, '<br>')}</p>
        </div>
      </div>

      <div class="section">
        <div class="info-row">
          <span class="info-label">Submission ID:</span>
          <span class="info-value" style="font-family: monospace; font-size: 11px;">${submission.id}</span>
        </div>
        <div class="info-row" style="border-bottom: none;">
          <span class="info-label">Submitted:</span>
          <span class="info-value">${new Date(submission.created_at).toLocaleString('en-US', { dateStyle: 'medium', timeStyle: 'short' })}</span>
        </div>
      </div>
    </div>
    <div class="footer">
      <p>This is an automated notification from your Richview Capital website consultation form.</p>
      <p>Please respond to the client within 24 hours.</p>
    </div>
  </div>
</body>
</html>
`;
}

function generateClientEmailHTML(submission: ConsultationSubmission): string {
  return `
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Consultation Request Received</title>
  <style>
    body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif; line-height: 1.6; color: #333; margin: 0; padding: 0; background-color: #f4f4f4; }
    .container { max-width: 600px; margin: 20px auto; background: #ffffff; border-radius: 8px; overflow: hidden; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }
    .header { background: linear-gradient(135deg, #0B1635 0%, #1a2845 100%); color: #ffffff; padding: 40px 20px; text-align: center; }
    .header h1 { margin: 0; font-size: 28px; font-weight: 600; }
    .header p { margin: 10px 0 0; font-size: 15px; opacity: 0.9; }
    .content { padding: 35px 25px; }
    .content p { margin: 0 0 16px; font-size: 15px; line-height: 1.6; }
    .highlight-box { background: #f9f9f9; border-left: 4px solid #ff6600; padding: 20px; margin: 20px 0; border-radius: 4px; }
    .info-item { margin-bottom: 10px; }
    .info-label { font-weight: 600; color: #0B1635; }
    .cta-button { display: inline-block; background: #ff6600; color: #ffffff; padding: 14px 30px; text-decoration: none; border-radius: 6px; font-weight: 600; margin: 20px 0; }
    .footer { background: #f9f9f9; padding: 25px; text-align: center; font-size: 13px; color: #666; line-height: 1.6; }
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <h1>Thank You, ${submission.first_name}!</h1>
      <p>We've received your consultation request</p>
    </div>
    <div class="content">
      <p>Hello ${submission.first_name},</p>

      <p>Thank you for reaching out to Richview Capital. We've successfully received your consultation request and our team will review it shortly.</p>

      <div class="highlight-box">
        <div class="info-item">
          <span class="info-label">Your Preferred Date:</span> ${new Date(submission.consultation_date).toLocaleDateString('en-US', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' })}
        </div>
        <div class="info-item">
          <span class="info-label">Your Preferred Time:</span> ${submission.consultation_time}
        </div>
      </div>

      <p><strong>What happens next?</strong></p>
      <ul style="margin: 10px 0 20px; padding-left: 20px;">
        <li style="margin-bottom: 8px;">Our team will review your request within 24 hours</li>
        <li style="margin-bottom: 8px;">We'll confirm your consultation appointment via email or phone</li>
        <li style="margin-bottom: 8px;">You'll receive a calendar invite with meeting details</li>
      </ul>

      <p>If you have any immediate questions, please don't hesitate to contact us at <a href="tel:+14163004448" style="color: #ff6600; text-decoration: none;">(416) 300-4448</a>.</p>

      <p style="margin-top: 30px;">Best regards,<br><strong>The Richview Capital Team</strong></p>
    </div>
    <div class="footer">
      <p><strong>Richview Capital MIC</strong><br>
      7681 Highway 27, Unit 15, Suite 200<br>
      Woodbridge, ON L4L 4M5</p>
      <p style="margin-top: 15px;">
        Phone: <a href="tel:+14163004448" style="color: #ff6600; text-decoration: none;">(416) 300-4448</a><br>
        Email: <a href="mailto:info@richviewcapital.ca" style="color: #ff6600; text-decoration: none;">info@richviewcapital.ca</a>
      </p>
      <p style="margin-top: 15px; font-size: 11px; color: #999;">
        Licensed MIC #13171
      </p>
    </div>
  </div>
</body>
</html>
`;
}

Deno.serve(async (req: Request) => {
  try {
    if (req.method === "OPTIONS") {
      return new Response(null, {
        status: 200,
        headers: corsHeaders,
      });
    }

    if (req.method !== "POST") {
      return new Response(
        JSON.stringify({ error: "Method not allowed" }),
        {
          status: 405,
          headers: {
            ...corsHeaders,
            "Content-Type": "application/json",
          },
        }
      );
    }

    const { submission } = await req.json();

    if (!submission) {
      return new Response(
        JSON.stringify({ error: "Submission data is required" }),
        {
          status: 400,
          headers: {
            ...corsHeaders,
            "Content-Type": "application/json",
          },
        }
      );
    }

    const adminEmailHTML = generateEmailHTML(submission);
    const clientEmailHTML = generateClientEmailHTML(submission);

    console.log("Email notifications prepared for:", {
      submissionId: submission.id,
      clientEmail: submission.email,
      clientName: `${submission.first_name} ${submission.last_name}`,
    });

    console.log(
      "\n=== ADMIN EMAIL (would be sent to: info@richviewcapital.ca) ===\n"
    );
    console.log("Subject: New Consultation Request from", submission.first_name, submission.last_name);

    console.log(
      "\n=== CLIENT EMAIL (would be sent to:",
      submission.email,
      ") ===\n"
    );
    console.log("Subject: Your Consultation Request - Richview Capital");

    return new Response(
      JSON.stringify({
        success: true,
        message: "Email notifications logged (email service not configured)",
        emails: {
          admin: {
            to: "info@richviewcapital.ca",
            subject: `New Consultation Request from ${submission.first_name} ${submission.last_name}`,
            sent: false,
            note: "Email service not configured - would send in production",
          },
          client: {
            to: submission.email,
            subject: "Your Consultation Request - Richview Capital",
            sent: false,
            note: "Email service not configured - would send in production",
          },
        },
      }),
      {
        status: 200,
        headers: {
          ...corsHeaders,
          "Content-Type": "application/json",
        },
      }
    );
  } catch (error) {
    console.error("Email function error:", error);
    return new Response(
      JSON.stringify({
        error: "Failed to process email notifications",
        details: error instanceof Error ? error.message : "Unknown error",
      }),
      {
        status: 500,
        headers: {
          ...corsHeaders,
          "Content-Type": "application/json",
        },
      }
    );
  }
});
