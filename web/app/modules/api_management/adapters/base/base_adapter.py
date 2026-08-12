from abc import ABC, abstractmethod


class BaseProviderAdapter(ABC):

    @abstractmethod
    async def test_connection(self):
        """API ulanishini tekshirish."""
        raise NotImplementedError

    @abstractmethod
    async def get_balance(self):
        """Provider balansini olish."""
        raise NotImplementedError

    @abstractmethod
    async def sync_services(self):
        """API xizmatlarini sinxronlash."""
        raise NotImplementedError

    @abstractmethod
    async def get_service(self, service_id: int):
        """Bitta xizmatni olish."""
        raise NotImplementedError

    @abstractmethod
    async def create_order(self, **kwargs):
        """Buyurtma yaratish."""
        raise NotImplementedError

    @abstractmethod
    async def get_order_status(self, order_id):
        """Buyurtma holatini olish."""
        raise NotImplementedError

    @abstractmethod
    async def cancel_order(self, order_id):
        """Buyurtmani bekor qilish."""
        raise NotImplementedError
