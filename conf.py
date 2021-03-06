import torch
import torchvision.transforms as T


def get_optim_scheduler(key, model, epoch=None):
    if (key == 'resnet'):
        optimizer = torch.optim.SGD(lr=0.1, momentum=0.9, weight_decay=1e-4, params=model.parameters())
        scheduler = torch.optim.lr_scheduler.MultiStepLR(optimizer=optimizer, milestones=[epoch // 3, 2 * epoch // 3],
                                                         gamma=0.1)
        train_transform = T.Compose([
            T.RandomHorizontalFlip(),
            T.ToTensor(),
            T.Normalize(
                (0.5070751592371323, 0.48654887331495095, 0.4409178433670343),
                (0.2673342858792401, 0.2564384629170883, 0.27615047132568404)),
        ])
        val_transform = T.Compose([
            T.ToTensor(),
            T.Normalize(
                (0.5070751592371323, 0.48654887331495095, 0.4409178433670343),
                (0.2673342858792401, 0.2564384629170883, 0.27615047132568404)),
        ])
        return optimizer, scheduler, train_transform, val_transform
    if (key == 'resnetcifar100'):
        optimizer = torch.optim.SGD(lr=0.1, momentum=0.9, weight_decay=5e-4, params=model.parameters())
        scheduler = StepLRScheduler(optimizer, decay_t=epoch // 4, decay_rate=2e-1, warmup_t=400, warmup_lr_init=0)
        # scheduler = torch.optim.lr_scheduler.MultiStepLR(optimizer, milestones=[60*400,120*400,160*400],gamma=0.2)  # learning rate decay
        train_transform = T.Compose([
            T.RandomCrop(32, padding=4),
            T.RandomHorizontalFlip(),
            T.RandomRotation(15),
            T.ToTensor(),
            T.Normalize(
                (0.5070751592371323, 0.48654887331495095, 0.4409178433670343),
                (0.2673342858792401, 0.2564384629170883, 0.27615047132568404)),
        ])
        val_transform = T.Compose([
            T.ToTensor(),
            T.Normalize(
                (0.5070751592371323, 0.48654887331495095, 0.4409178433670343),
                (0.2673342858792401, 0.2564384629170883, 0.27615047132568404)),
        ])
        return optimizer, scheduler, train_transform, val_transform
    if (key == 'own'):
        optimizer = torch.optim.SGD(lr=0.1, momentum=0.9, weight_decay=1e-3, params=model.parameters())
        scheduler = StepLRScheduler(optimizer, decay_t=epoch // 4, decay_rate=2e-1, warmup_t=400, warmup_lr_init=0)
        train_transform = T.Compose([
            T.RandomCrop(32, padding=4),
            T.RandomHorizontalFlip(),
            T.RandomRotation(15),
            T.ColorJitter(),
            T.RandomAutocontrast(),
            T.RandomGrayscale(),
            T.RandomVerticalFlip(),
            T.ToTensor(),
            T.RandomErasing(),
            T.Normalize(
                (0.5070751592371323, 0.48654887331495095, 0.4409178433670343),
                (0.2673342858792401, 0.2564384629170883, 0.27615047132568404)),
        ])
        val_transform = T.Compose([
            T.ToTensor(),
            T.Normalize(
                (0.5070751592371323, 0.48654887331495095, 0.4409178433670343),
                (0.2673342858792401, 0.2564384629170883, 0.27615047132568404)),
        ])
        return optimizer, scheduler, train_transform, val_transform
    else:
        raise NotImplementedError


from timm.scheduler.step_lr import StepLRScheduler
from timm import create_model

if __name__ == "__main__":
    model = create_model('resnet34')
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-1)
    scheduler = StepLRScheduler(optimizer, decay_t=10, decay_rate=2e-1, warmup_t=5, warmup_lr_init=0)
    for e in range(100):
        scheduler.step(e)
        print(e, scheduler.optimizer.param_groups[0]['lr'])
