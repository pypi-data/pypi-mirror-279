@prompt
    @context
        You are an experienced Python software developer.
    @end

    @objective
        Code-review & refactor below code to make it more readable and maintainable.
        ```python
        now = time.time()
        if not args.stream:
            try:
                response = get_sync_response(args, console, serialized_data)
            except APIConnectionError:
                console.print(
                    "Error connecting to provider API. Try again! Please turn-off the VPN if needed.",
                    style = "bold red"
                )
                return
            # Print the completion with rich console
            if args.raw:
                console.print(response)
            else:
                console.print(Panel(Markdown(response, "\n")), soft_wrap=True, new_line_start=True)
                console.print(f"\nTime taken: {time.time() - now} seconds", style="bold green")
        else:
            with Live(refresh_per_second=4) as live:
                message = ""
                for chunk in get_stream_response(args, console, serialized_data):
                    if chunk:
                        message += chunk
                        markdown_content = Markdown(message, "\n")
                        panel = Panel(markdown_content)
                        live.update(panel)

            if not args.raw:
                console.print(f"\nTime taken: {time.time() - now} seconds", style="bold green")
        ```
    @end
@end
