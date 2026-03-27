const corsHeaders = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
  "Access-Control-Allow-Headers":
    "Content-Type, Authorization, X-Client-Info, Apikey",
};

interface WebhookPayload {
  submission: {
    id: string;
    first_name: string;
    last_name: string;
    email: string;
    phone: string;
    interest: string;
    message: string;
    consultation_date: string;
    consultation_time: string;
    status: string;
    created_at: string;
  };
  event: string;
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

    const payload: WebhookPayload = await req.json();

    console.log("\n=== WEBHOOK TRIGGERED ===");
    console.log("Event:", payload.event);
    console.log("Submission ID:", payload.submission.id);
    console.log("Client:", payload.submission.first_name, payload.submission.last_name);
    console.log("Email:", payload.submission.email);
    console.log("Phone:", payload.submission.phone);
    console.log("Interest:", payload.submission.interest);
    console.log("Consultation:", payload.submission.consultation_date, "at", payload.submission.consultation_time);
    console.log("Status:", payload.submission.status);
    console.log("Timestamp:", new Date(payload.submission.created_at).toISOString());
    console.log("========================\n");

    const webhookData = {
      event: payload.event,
      timestamp: new Date().toISOString(),
      data: {
        submission_id: payload.submission.id,
        client_name: `${payload.submission.first_name} ${payload.submission.last_name}`,
        client_email: payload.submission.email,
        client_phone: payload.submission.phone,
        interest_type: payload.submission.interest,
        consultation_datetime: `${payload.submission.consultation_date} ${payload.submission.consultation_time}`,
        message_preview: payload.submission.message.substring(0, 100) + (payload.submission.message.length > 100 ? "..." : ""),
        status: payload.submission.status,
        created_at: payload.submission.created_at,
      },
    };

    console.log("Webhook payload prepared:", JSON.stringify(webhookData, null, 2));

    return new Response(
      JSON.stringify({
        success: true,
        message: "Webhook processed successfully",
        webhook: {
          event: payload.event,
          processed_at: new Date().toISOString(),
          submission_id: payload.submission.id,
          note: "Webhook logged - configure external webhook URL in production",
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
    console.error("Webhook error:", error);
    return new Response(
      JSON.stringify({
        error: "Failed to process webhook",
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
