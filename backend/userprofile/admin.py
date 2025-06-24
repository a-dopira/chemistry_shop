from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.sessions.models import Session
from django.contrib import messages
from django.utils import timezone
from django.utils.html import format_html
from .models import User, UserProfile
from .activation import ActivationEmail

from rest_framework_simplejwt.token_blacklist.models import (
    OutstandingToken,
    BlacklistedToken,
)


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = "Профиль"
    fields = ("address", "phone_number", "userphoto", "created_at", "updated_at")
    readonly_fields = ("created_at", "updated_at")


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)

    list_display = (
        "email",
        "username",
        "is_active",
        "is_staff",
        "email_verified_status",
        "active_sessions_count",
        "active_jwt_tokens_count",
        "date_joined",
        "last_login",
    )

    list_filter = ("is_active", "is_staff", "is_superuser", "date_joined", "last_login")

    search_fields = ("email", "username", "first_name", "last_name")
    ordering = ("-date_joined",)

    fieldsets = BaseUserAdmin.fieldsets + (
        ("Extra", {"fields": ("email_verified_at",)}),
    )

    readonly_fields = ("date_joined", "last_login")

    def email_verified_status(self, obj):
        if obj.email_verified_at:
            return format_html(
                '<span style="color: green;">✅ Active {}</span>',
                obj.email_verified_at.strftime("%d.%m.%Y %H:%M"),
            )
        return format_html('<span style="color: red;">❌ Inactive</span>')

    email_verified_status.short_description = "Email active"

    def active_sessions_count(self, obj):

        count = Session.objects.filter(
            expire_date__gte=timezone.now(),
            session_data__contains=f'"_auth_user_id":"{obj.pk}"',
        ).count()

        if count > 0:
            return format_html(
                '<span style="color: orange; font-weight: bold;"> {} web</span>', count
            )
        return format_html('<span style="color: gray;">no sessions</span>')

    active_sessions_count.short_description = "Web sessions"

    def active_jwt_tokens_count(self, obj):
        try:
            outstanding_tokens = OutstandingToken.objects.filter(user=obj)

            blacklisted_token_ids = BlacklistedToken.objects.filter(
                token__user=obj
            ).values_list("token_id", flat=True)

            active_tokens = outstanding_tokens.exclude(id__in=blacklisted_token_ids)
            count = active_tokens.count()

            if count > 0:
                return format_html(
                    '<span style="color: blue; font-weight: bold;"> {} API</span>',
                    count,
                )
            return format_html('<span style="color: gray;">no jwt</span>')

        except Exception:
            return format_html('<span style="color: red;">jwt error</span>')

    active_jwt_tokens_count.short_description = "JWT tokens"

    actions = [
        "activate_users",
        "deactivate_users",
        "logout_web_sessions_only",
        "revoke_jwt_tokens_only",
        "logout_all_user_sessions",
        "emergency_logout_everything",
        "resend_activation_emails",
    ]

    def activate_users(self, request, queryset):
        updated = queryset.update(is_active=True, email_verified_at=timezone.now())
        self.message_user(request, f"Activated {updated} users.", messages.SUCCESS)

    activate_users.short_description = "Activate selected users"

    def deactivate_users(self, request, queryset):
        queryset = queryset.exclude(is_superuser=True)
        updated = queryset.update(is_active=False)

        total_sessions = 0
        total_tokens = 0

        for user in queryset:
            sessions = Session.objects.filter(
                expire_date__gte=timezone.now(),
                session_data__contains=f'"_auth_user_id":"{user.pk}"',
            )
            total_sessions += sessions.count()
            sessions.delete()

            try:
                outstanding_tokens = OutstandingToken.objects.filter(user=user)
                blacklisted_token_ids = BlacklistedToken.objects.filter(
                    token__user=user
                ).values_list("token_id", flat=True)

                active_tokens = outstanding_tokens.exclude(id__in=blacklisted_token_ids)

                for token in active_tokens:
                    BlacklistedToken.objects.get_or_create(token=token)
                    total_tokens += 1
            except Exception:
                pass

        self.message_user(
            request,
            f"Deactivated {updated} users. "
            f"Expired {total_sessions} web sessions and blacklisted {total_tokens} JWT tokens.",
            messages.WARNING,
        )

    deactivate_users.short_description = "Deactivate"

    def logout_web_sessions_only(self, request, queryset):
        total_sessions = 0
        user_count = 0

        for user in queryset:
            sessions = Session.objects.filter(
                expire_date__gte=timezone.now(),
                session_data__contains=f'"_auth_user_id":"{user.pk}"',
            )
            session_count = sessions.count()
            if session_count > 0:
                sessions.delete()
                total_sessions += session_count
                user_count += 1

        if total_sessions > 0:
            self.message_user(
                request,
                f"Expired {total_sessions} web sessions for {user_count} users. "
                f"JWT tokens are not affected.",
                messages.WARNING,
            )
        else:
            self.message_user(
                request, "Web sessions are already expired.", messages.INFO
            )

    logout_web_sessions_only.short_description = "Expire web sessions only"

    def revoke_jwt_tokens_only(self, request, queryset):
        total_tokens = 0
        user_count = 0

        for user in queryset:
            try:
                outstanding_tokens = OutstandingToken.objects.filter(user=user)
                blacklisted_token_ids = BlacklistedToken.objects.filter(
                    token__user=user
                ).values_list("token_id", flat=True)

                active_tokens = outstanding_tokens.exclude(id__in=blacklisted_token_ids)

                for token in active_tokens:
                    BlacklistedToken.objects.get_or_create(token=token)
                    total_tokens += 1

                if active_tokens.exists():
                    user_count += 1
            except Exception:
                continue

        if total_tokens > 0:
            self.message_user(
                request,
                f"Blacklisted {total_tokens} JWT tokens for {user_count} users. "
                f"Web sessions are still active.",
                messages.WARNING,
            )
        else:
            self.message_user(
                request, "Selected users have no active JWT tokens.", messages.INFO
            )

    revoke_jwt_tokens_only.short_description = "Blacklist JWT tokens only"

    def logout_all_user_sessions(self, request, queryset):
        total_sessions = 0
        total_tokens = 0
        user_count = 0

        for user in queryset:
            had_activity = False

            sessions = Session.objects.filter(
                expire_date__gte=timezone.now(),
                session_data__contains=f'"_auth_user_id":"{user.pk}"',
            )
            session_count = sessions.count()
            if session_count > 0:
                sessions.delete()
                total_sessions += session_count
                had_activity = True

            try:
                outstanding_tokens = OutstandingToken.objects.filter(user=user)
                blacklisted_token_ids = BlacklistedToken.objects.filter(
                    token__user=user
                ).values_list("token_id", flat=True)

                active_tokens = outstanding_tokens.exclude(id__in=blacklisted_token_ids)

                for token in active_tokens:
                    BlacklistedToken.objects.get_or_create(token=token)
                    total_tokens += 1
                    had_activity = True
            except Exception:
                pass

            if had_activity:
                user_count += 1

        if user_count > 0:
            jwt_status = f" and blacklisted {total_tokens} JWT tokens"
            self.message_user(
                request,
                f"Completed logout for {user_count} users. "
                f"Exited {total_sessions} web sessions{jwt_status}.",
                messages.WARNING,
            )
        else:
            self.message_user(
                request, "No active sessions found for selected users.", messages.INFO
            )

    logout_all_user_sessions.short_description = "Exit all user sessions and tokens"

    def emergency_logout_everything(self, request, queryset):
        all_sessions = Session.objects.filter(expire_date__gte=timezone.now())
        session_count = all_sessions.count()
        all_sessions.delete()

        token_count = 0
        try:
            outstanding_tokens = OutstandingToken.objects.all()
            blacklisted_token_ids = BlacklistedToken.objects.values_list(
                "token_id", flat=True
            )

            active_tokens = outstanding_tokens.exclude(id__in=blacklisted_token_ids)

            for token in active_tokens:
                BlacklistedToken.objects.get_or_create(token=token)
                token_count += 1
        except Exception:
            pass

        jwt_msg = f" and blacklisted {token_count} JWT tokens"

        self.message_user(
            request,
            f"Emergency logout: exited {session_count} web sessions{jwt_msg}. "
            f"All JWT tokens are now blacklisted.",
            messages.ERROR,
        )

    emergency_logout_everything.short_description = "Emergency logout everything"

    def resend_activation_emails(self, request, queryset):
        """Повторно отправить письма активации через Djoser"""
        sent_count = 0
        error_count = 0
        already_active_count = 0

        for user in queryset:
            if user.is_active:
                already_active_count += 1
                continue

            try:
                context = {"user": user}
                email_instance = ActivationEmail(request=request, context=context)
                email_instance.send([user.email])
                sent_count += 1
            except Exception as e:
                error_count += 1

        if sent_count > 0:
            self.message_user(
                request, f"Отправлено {sent_count} писем активации.", messages.SUCCESS
            )

        if already_active_count > 0:
            self.message_user(
                request,
                f"Пропущено {already_active_count} уже активированных.",
                messages.INFO,
            )

        if error_count > 0:
            self.message_user(
                request,
                f"Ошибка отправки {error_count} писем активации.",
                messages.ERROR,
            )

    resend_activation_emails.short_description = "Resend activation emails"


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "user_email",
        "user_status",
        "has_address",
        "has_phone",
        "has_photo",
        "created_at",
        "updated_at",
    )

    list_filter = ("created_at", "updated_at")
    search_fields = ("user__email", "user__username", "address", "phone_number")
    readonly_fields = ("created_at", "updated_at")

    def user_email(self, obj):
        return obj.user.email

    user_email.short_description = "Email"

    def user_status(self, obj):
        if obj.user.is_active:
            return format_html('<span style="color: green;">✅ Active</span>')
        return format_html('<span style="color: red;">❌ Inactive</span>')

    user_status.short_description = "Статус"

    def has_address(self, obj):
        return "✅" if obj.address else "❌"

    has_address.short_description = "Address"

    def has_phone(self, obj):
        return "✅" if obj.phone_number else "❌"

    has_phone.short_description = "Phone"

    def has_photo(self, obj):
        return "✅" if obj.userphoto else "❌"

    has_photo.short_description = "Photo"


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = (
        "session_key_short",
        "user_info",
        "expire_date",
        "is_active",
        "age_in_days",
    )

    list_filter = ("expire_date",)
    search_fields = ("session_key",)
    ordering = ("-expire_date",)

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}

        now = timezone.now()
        total_sessions = Session.objects.count()
        active_sessions = Session.objects.filter(expire_date__gte=now).count()
        expired_sessions = Session.objects.filter(expire_date__lt=now).count()

        old_cutoff = now - timezone.timedelta(days=30)
        very_old_sessions = Session.objects.filter(expire_date__lt=old_cutoff).count()

        extra_context.update(
            {
                "session_stats": {
                    "total": total_sessions,
                    "active": active_sessions,
                    "expired": expired_sessions,
                    "very_old": very_old_sessions,
                }
            }
        )

        return super().changelist_view(request, extra_context)

    def session_key_short(self, obj):
        return f"{obj.session_key[:10]}..."

    session_key_short.short_description = "Session key"

    def user_info(self, obj):
        try:
            session_data = obj.get_decoded()
            user_id = session_data.get("_auth_user_id")
            if user_id:
                try:
                    from .models import User

                    user = User.objects.get(pk=user_id)
                    return format_html(
                        "<strong>{}</strong><br><small>{}</small>",
                        user.username,
                        user.email,
                    )
                except User.DoesNotExist:
                    return "User not found"
            return "Anonymous user"
        except:
            return "Decoding error"

    user_info.short_description = "User"

    def is_active(self, obj):
        if obj.expire_date > timezone.now():
            return format_html('<span style="color: green;">🟢 Active</span>')
        return format_html('<span style="color: red;">🔴 Expired</span>')

    is_active.short_description = "Статус"

    def age_in_days(self, obj):
        now = timezone.now()
        if obj.expire_date > now:
            days_left = (obj.expire_date - now).days
            return format_html(
                '<span style="color: green;">Expires in {} days</span>', days_left
            )
        else:
            days_ago = (now - obj.expire_date).days
            if days_ago == 0:
                return format_html('<span style="color: orange;">Today</span>')
            elif days_ago < 7:
                return format_html(
                    '<span style="color: orange;">{} days ago</span>', days_ago
                )
            else:
                return format_html(
                    '<span style="color: red;">{} days ago</span>', days_ago
                )

    age_in_days.short_description = "Возраст"

    actions = [
        "delete_expired_sessions",
        "delete_old_sessions",
        "delete_very_old_sessions",
        "delete_selected_sessions",
    ]

    def delete_expired_sessions(self, request, queryset):

        expired = Session.objects.filter(expire_date__lt=timezone.now())
        count = expired.count()
        expired.delete()
        self.message_user(
            request, f"Deleted {count} expired sessions.", level=messages.SUCCESS
        )

    delete_expired_sessions.short_description = "Delete expired sessions"

    def delete_old_sessions(self, request, queryset):
        cutoff = timezone.now() - timezone.timedelta(days=7)
        old_sessions = Session.objects.filter(expire_date__lt=cutoff)
        count = old_sessions.count()
        old_sessions.delete()
        self.message_user(
            request,
            f"Deleted {count} sessions older than 7 days.",
            level=messages.SUCCESS,
        )

    delete_old_sessions.short_description = "Delete sessions older than 7 days"

    def delete_very_old_sessions(self, request, queryset):
        cutoff = timezone.now() - timezone.timedelta(days=30)
        very_old_sessions = Session.objects.filter(expire_date__lt=cutoff)
        count = very_old_sessions.count()
        very_old_sessions.delete()
        self.message_user(
            request,
            f"Deleted {count} sessions older than 30 days.",
            level=messages.SUCCESS,
        )

    delete_very_old_sessions.short_description = "Delete sessions older than 30 days"

    def delete_selected_sessions(self, request, queryset):
        count = queryset.count()
        queryset.delete()
        self.message_user(request, f"Deleted {count} sessions.", level=messages.WARNING)

    delete_selected_sessions.short_description = "Delete selected sessions"
