from datetime import datetime, timezone
def create_related_items(model, data_list, business, now):
    now = datetime.now(timezone.utc)
    return [
        model(
            **item.model_dump(exclude_unset=True),
            created_at=item.created_at or now,
            updated_at=None,
            business=business
        )
        for item in data_list or []
    ]