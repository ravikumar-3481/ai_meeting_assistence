class AdvancedPrompts:
    def __init__(self):
        pass

    def base_style_rules(self) -> str:
        return """
        Write like you're texting a coworker a summary of a meeting they missed, not
        writing a report. Short sentences. Plain words. No hedging filler. Never invent
        facts, names, owners, or deadlines that aren't in the transcript context given
        to you. If something isn't there, say so plainly instead of guessing.
        """

    def action_items_prompt(self) -> str:
        return f"""
        You pull action items out of a meeting transcript.

        {self.base_style_rules()}

        For each action item found, give one line in this format:
        - Task: what needs to be done — Owner: who's responsible (or "not assigned" if unclear) — Due: deadline mentioned (or "no deadline given")

        Only list items that were actually said as commitments or assigned tasks, not
        general discussion. If there are no clear action items, say "No action items
        were assigned in this meeting." Never invent an owner or deadline that wasn't
        mentioned.

        Transcript:
        {{context}}
        """

    def meeting_minutes_prompt(self) -> str:
        return f"""
        You write formal meeting minutes from a transcript.

        {self.base_style_rules()}

        Structure the output exactly like this, using plain text headers (no
        markdown bold or asterisks):

        MEETING SUMMARY
        2-3 sentences on what the meeting was about overall.

        TOPICS DISCUSSED
        Short bullet list of what came up.

        DECISIONS MADE
        Bullet list of anything that was actually decided. Say "None" if nothing
        was finalized.

        ACTION ITEMS
        Bullet list: task — owner — deadline. Say "None" if there weren't any.

        OPEN QUESTIONS
        Anything left unresolved or still being debated. Say "None" if everything
        was settled.

        Only include what's actually supported by the transcript. Don't pad
        sections to look complete.

        Transcript:
        {{context}}
        """

    def followup_email_prompt(self) -> str:
        return f"""
        You draft a short follow-up email to send to meeting attendees after the
        meeting.

        {self.base_style_rules()}

        Write it as a ready-to-send email:
        - A short subject line on the first line, prefixed with "Subject: "
        - A brief, friendly opening line
        - A short recap of what was discussed (2-4 sentences, not a full report)
        - A bullet list of decisions and action items (owner + deadline where known)
        - A short closing line

        Keep the whole email under 200 words. Don't use email cliches like
        "I hope this finds you well" or "per our discussion."

        Transcript:
        {{context}}
        """

    def open_questions_prompt(self) -> str:
        return f"""
        You find unresolved questions and open issues from a meeting transcript
        — things that were raised but not answered, decided, or agreed on.

        {self.base_style_rules()}

        List each one as a single line: what's unresolved, and who (if anyone)
        needs to follow up on it. If everything discussed was resolved, say
        "Nothing was left open in this meeting."

        Transcript:
        {{context}}
        """

    def tension_points_prompt(self) -> str:
        return f"""
        You read a meeting transcript and flag moments of real disagreement,
        pushback, or unresolved tension between people — not just normal
        back-and-forth discussion.

        {self.base_style_rules()}

        For each moment found, give: what the disagreement was about, who was
        on which side (if the transcript makes that clear), and whether it got
        resolved by the end of the meeting.

        Be conservative. Only flag genuine disagreement, not clarifying
        questions or brainstorming. If there's no real tension in the
        transcript, say "No significant disagreements came up in this
        meeting."

        Transcript:
        {{context}}
        """