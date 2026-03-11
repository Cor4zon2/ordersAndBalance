from core.domain.entities import UserEntity
from core.infrastructure.models import User, Wallet
from core.domain.interfaces import IUserRepository

from typing import Optional

class DjangoUserRepository(IUserRepository):
    def get_user(self, user_id: int) -> Optional[UserEntity]:
        user = User.objects.filter(id = user_id).values("id", "name", "email").last()
        wallet = Wallet.objects.filter(user_id = user_id).values("id", "balance").last()
        
        return UserEntity(
            id=user["id"],
            name=user["name"],
            email=user["email"],
            wallet_id=wallet["id"],
            wallet_balance=wallet["balance"]
        )