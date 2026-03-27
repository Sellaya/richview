import { createClient } from "npm:@supabase/supabase-js@2";

const corsHeaders = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
  "Access-Control-Allow-Headers":
    "Content-Type, Authorization, X-Client-Info, Apikey",
};

interface ConsultationSubmission {
  first_name: string;
  last_name: string;
  email: string;
  phone: string;
  interest: string;
  message: string;
  consultation_date: string;
  consultation_time: string;
  user_agent?: string;
  ip_address?: string;
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

    const supabaseUrl = Deno.env.get("SUPABASE_URL")!;
    const supabaseServiceKey = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!;
    const supabase = createClient(supabaseUrl, supabaseServiceKey);

    const body: ConsultationSubmission = await req.json();

    const userAgent = req.headers.get("user-agent") || "";
    const forwardedFor = req.headers.get("x-forwarded-for");
    const ipAddress = forwardedFor
      ? forwardedFor.split(",")[0].trim()
      : req.headers.get("x-real-ip") || "";

    const { data, error } = await supabase
      .from("consultation_submissions")
      .insert({
        first_name: body.first_name,
        last_name: body.last_name,
        email: body.email,
        phone: body.phone,
        interest: body.interest,
        message: body.message,
        consultation_date: body.consultation_date,
        consultation_time: body.consultation_time,
        user_agent: userAgent,
        ip_address: ipAddress || null,
        status: "pending",
        source: "website",
      })
      .select()
      .single();

    if (error) {
      console.error("Database error:", error);
      return new Response(
        JSON.stringify({ error: "Failed to submit consultation request" }),
        {
          status: 500,
          headers: {
            ...corsHeaders,
            "Content-Type": "application/json",
          },
        }
      );
    }

    try {
      const emailFunctionUrl = `${supabaseUrl}/functions/v1/send-consultation-email`;
      await fetch(emailFunctionUrl, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${supabaseServiceKey}`,
        },
        body: JSON.stringify({
          submission: data,
        }),
      });
    } catch (emailError) {
      console.error("Email notification failed:", emailError);
    }

    try {
      const webhookFunctionUrl = `${supabaseUrl}/functions/v1/consultation-webhook`;
      await fetch(webhookFunctionUrl, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${supabaseServiceKey}`,
        },
        body: JSON.stringify({
          submission: data,
          event: "consultation.created",
        }),
      });
    } catch (webhookError) {
      console.error("Webhook notification failed:", webhookError);
    }

    return new Response(
      JSON.stringify({
        success: true,
        message: "Consultation request submitted successfully",
        id: data.id,
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
    console.error("Unexpected error:", error);
    return new Response(
      JSON.stringify({
        error: "An unexpected error occurred",
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
