<?php

namespace App\Entity;

use App\Repository\ReservationRepository;
use Doctrine\Common\Collections\ArrayCollection;
use Doctrine\Common\Collections\Collection;
use Doctrine\DBAL\Types\Types;
use Doctrine\ORM\Mapping as ORM;

#[ORM\Entity(repositoryClass: ReservationRepository::class)]
class Reservation
{
    #[ORM\Id]
    #[ORM\GeneratedValue]
    #[ORM\Column]
    private ?int $id = null;

    #[ORM\OneToOne(inversedBy: 'reservation', cascade: ['persist', 'remove'])]
    #[ORM\JoinColumn(nullable: false)]
    private ?user $idUser = null;

    #[ORM\Column(type: Types::DATETIME_MUTABLE)]
    private ?\DateTimeInterface $date = null;

    #[ORM\Column]
    private ?\DateInterval $durée = null;

    #[ORM\Column]
    private ?int $quantity = null;

    #[ORM\Column]
    private ?float $prixtot = null;

    #[ORM\OneToMany(targetEntity: items::class, mappedBy: 'reservation', orphanRemoval: true)]
    private Collection $idItems;

    public function __construct()
    {
        $this->idItems = new ArrayCollection();
    }

    public function getId(): ?int
    {
        return $this->id;
    }

    public function getIdUser(): ?user
    {
        return $this->idUser;
    }

    public function setIdUser(user $idUser): static
    {
        $this->idUser = $idUser;

        return $this;
    }

    public function getDate(): ?\DateTimeInterface
    {
        return $this->date;
    }

    public function setDate(\DateTimeInterface $date): static
    {
        $this->date = $date;

        return $this;
    }

    public function getDurée(): ?\DateInterval
    {
        return $this->durée;
    }

    public function setDurée(\DateInterval $durée): static
    {
        $this->durée = $durée;

        return $this;
    }

    public function getQuantity(): ?int
    {
        return $this->quantity;
    }

    public function setQuantity(int $quantity): static
    {
        $this->quantity = $quantity;

        return $this;
    }

    public function getPrixtot(): ?float
    {
        return $this->prixtot;
    }

    public function setPrixtot(float $prixtot): static
    {
        $this->prixtot = $prixtot;

        return $this;
    }

    /**
     * @return Collection<int, items>
     */
    public function getIdItems(): Collection
    {
        return $this->idItems;
    }

    public function addIdItem(items $idItem): static
    {
        if (!$this->idItems->contains($idItem)) {
            $this->idItems->add($idItem);
            $idItem->setReservation($this);
        }

        return $this;
    }

    public function removeIdItem(items $idItem): static
    {
        if ($this->idItems->removeElement($idItem)) {
            // set the owning side to null (unless already changed)
            if ($idItem->getReservation() === $this) {
                $idItem->setReservation(null);
            }
        }

        return $this;
    }
}
